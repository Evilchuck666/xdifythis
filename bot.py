import tweepy
import os
import random
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv("API_KEY")
apiSecret = os.getenv("API_SECRET")

accessToken = os.getenv("ACCESS_TOKEN")
accessTokenSecret = os.getenv("ACCESS_TOKEN_SECRET")

userName = os.getenv("USER_NAME")
lastIdFile = os.getenv("LAST_ID_FILE")

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
    if user_to_reply.lower() == userName.lower():
        return True
    return False


def they_want_to_insult_kreator(user_to_reply):
    if user_to_reply.lower() == os.getenv("MY_KREATOR").lower():
        return True
    return False


def get_random_tease_text():
    tease_dir = os.getenv("TEASES_TEXT_DIR")
    filename = random.choice(os.listdir(tease_dir))

    path = os.path.join(tease_dir, filename)
    text_file = open(path, "r")
    text_content = text_file.read()
    text_file.close()
    return text_content


def tweet_tease(reply_id):
    image_file = get_random_image(os.getenv("TEASES_IMAGE_DIR"))
    media = api.media_upload(filename=image_file)
    tease = get_random_tease_text()
    api.update_status(
        status=tease,
        media_ids=[media.media_id],
        in_reply_to_status_id=reply_id,
        auto_populate_reply_metadata=True
    )


def tweet_dont_dare(reply_id):
    image_file = get_random_image(os.getenv("DONT_DIR"))
    media = api.media_upload(filename=image_file)
    api.update_status(
        status="",
        media_ids=[media.media_id],
        in_reply_to_status_id=reply_id,
        auto_populate_reply_metadata=True
    )


def quote_tweet(reply):
    mentioned_user = "@{}".format(reply.user.screen_name)

    parent_tweet = reply.in_reply_to_status_id
    if parent_tweet is None:
        parent_tweet = reply.id

    try:
        tweet = api.get_status(parent_tweet, tweet_mode="extended")
        reply_to_user = tweet.user.screen_name
    except tweepy.Forbidden as e:
        if e.api_codes[0] == 179:
            reply_to_user = reply.entities["user_mentions"][0]["screen_name"]
        else:
            raise e

    if am_i_getting_xdified(reply_to_user):
        tweet_tease(reply.id)
        return

    if they_want_to_insult_kreator(reply_to_user):
        tweet_dont_dare(reply.id)
        return

    url = baseTwitterStatusUrl.format(reply_to_user, parent_tweet)
    image_file = get_random_image(os.getenv("MEMES_DIR"))
    media = api.media_upload(filename=image_file)
    api.update_status(status=mentioned_user, media_ids=[media.media_id], attachment_url=url)


def get_timeline():
    last_id = get_last_tweet()

    replies = api.search_tweets(q=userName, since_id=last_id, tweet_mode="extended")
    if len(replies) == 0:
        print("No new tweets! D:")
        return

    for reply in replies:
        quote_tweet(reply)


if __name__ == "__main__":
    get_timeline()
