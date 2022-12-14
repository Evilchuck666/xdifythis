import os
import random

import tweepy
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("API_KEY")
apiSecret = os.getenv("API_SECRET")

accessToken = os.getenv("ACCESS_TOKEN")
accessTokenSecret = os.getenv("ACCESS_TOKEN_SECRET")

my_kreator = os.getenv("MY_KREATOR").lower()
userName = os.getenv("USER_NAME")

auth = tweepy.OAuth1UserHandler(apiKey, apiSecret, accessToken, accessTokenSecret)
api = tweepy.API(auth)

baseTwitterStatusUrl = "https://twitter.com/{}/status/{}"


def get_random_image(img_dir):
    filename = random.choice(os.listdir(img_dir))
    path = os.path.join(img_dir, filename)
    return path


def get_last_tweet():
    last_id = api.user_timeline(screen_name=userName, count=1)[0].id
    return last_id


def am_i_getting_xdified(user_to_reply):
    return user_to_reply.lower() == userName.lower()


def they_want_to_insult_kreator(user_to_reply):
    return user_to_reply.lower() == my_kreator


def get_random_tease_text():
    tease_dir = os.getenv("TEASES_TEXT_DIR")
    filename = random.choice(os.listdir(tease_dir))

    path = os.path.join(tease_dir, filename)
    text_file = open(path, "r")
    text_content = text_file.read()
    text_file.close()
    return text_content


def tweet_tease(tweet_id):
    image_file = get_random_image(os.getenv("TEASES_IMAGE_DIR"))
    media = api.media_upload(filename=image_file)
    tease = get_random_tease_text()
    api.update_status(status=tease, media_ids=[media.media_id], in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)


def tweet_dont_dare(tweet_id):
    image_file = get_random_image(os.getenv("DONT_DIR"))
    media = api.media_upload(filename=image_file)
    api.update_status(status="", media_ids=[media.media_id], in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)


def its_just_a_retweet(tweet):
    none_reply_screen_name = tweet.in_reply_to_screen_name is None
    none_reply_status_id = tweet.in_reply_to_status_id is None
    none_reply_status_id_str = tweet.in_reply_to_status_id_str is None
    none_reply_user_id = tweet.in_reply_to_user_id is None
    none_reply_user_id_str = tweet.in_reply_to_user_id_str is None

    result = none_reply_screen_name and none_reply_status_id and none_reply_status_id_str
    result = result and none_reply_user_id and none_reply_user_id_str

    return result


def ignore_tweet(tweet):
    first_user = tweet.full_text[tweet.display_text_range[0]:].lower()
    if userName not in first_user:
        return True
    else:
        tweet_text = tweet.full_text[tweet.display_text_range[0]:].lower()
        stripped_text = tweet_text.strip()
        return stripped_text != "@xdifythis play"


def write_tweet(reply_to_user, parent_tweet, mentioned_user):
    url = baseTwitterStatusUrl.format(reply_to_user, parent_tweet)
    image_file = get_random_image(os.getenv("MEMES_DIR"))
    media = api.media_upload(filename=image_file)
    api.update_status(status=mentioned_user, media_ids=[media.media_id], attachment_url=url)


def fav_tweet(tweet):
    if not tweet.favorited:
        tweet.favorite()


def tweet_candado(tweet_id):
    image_file = get_random_image(os.getenv("CHAIN_DIR"))
    media = api.media_upload(filename=image_file)
    api.update_status(status="Cuenta candado...", media_ids=[media.media_id], in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
    return


def quote_tweet(tweet):
    mentioned_user = "@{}".format(tweet.user.screen_name)

    if ignore_tweet(tweet) or its_just_a_retweet(tweet):
        return

    parent_tweet = tweet.in_reply_to_status_id
    if parent_tweet is None:
        parent_tweet = tweet.id

    try:
        answer_tweet = api.get_status(parent_tweet, tweet_mode="extended")
        reply_to_user = answer_tweet.user.screen_name

        if am_i_getting_xdified(reply_to_user):
            tweet_tease(answer_tweet.id)
            return

        if they_want_to_insult_kreator(reply_to_user):
            tweet_dont_dare(answer_tweet.id)
            return

        write_tweet(reply_to_user, parent_tweet, mentioned_user)
        fav_tweet(tweet)
    except tweepy.Forbidden:
        return tweet_candado(tweet.id)


def get_timeline():
    tweets = get_latest_tweets()

    for tweet in tweets:
        quote_tweet(tweet)


def get_latest_tweets():
    last_id = get_last_tweet()
    query = "{} play -filter:retweets".format(userName)
    replies = api.search_tweets(q=query, since_id=last_id, tweet_mode="extended")
    if len(replies) == 0:
        print("No new tweets! D:")
    return replies


if __name__ == "__main__":
    get_timeline()
