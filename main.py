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


def get_random_image():
    image_dir = "images"
    filename = random.choice(os.listdir(image_dir))
    path = os.path.join(image_dir, filename)
    return path


def get_last_tweet():
    last_id = api.user_timeline(screen_name=userName, count=1)[0].id
    return last_id


def am_i_getting_xdified(user_to_reply):
    if user_to_reply.lower() == userName.lower():
        return True
    return False


def get_random_tease():
    tease_dir = "teases"
    filename = random.choice(os.listdir(tease_dir))

    while not (filename.endswith(".txt")):
        filename = random.choice(os.listdir(tease_dir))

    path = os.path.join(tease_dir, filename)
    text_file = open(path, "r")
    text_content = text_file.read()
    text_file.close()
    return text_content


def tweet_justin(reply_id):
    media = api.media_upload(filename=os.getenv("JUSTIN_FILE"))
    tease = get_random_tease()
    api.update_status(
        status=tease,
        media_ids=[media.media_id],
        in_reply_to_status_id=reply_id,
        auto_populate_reply_metadata=True
    )


def quote_tweet(reply):
    parent_tweet = reply.in_reply_to_status_id
    mentioned_user = "@{}".format(reply.user.screen_name)

    try:
        tweet = api.get_status(parent_tweet, tweet_mode="extended")
        reply_to_user = tweet.user.screen_name
    except tweepy.Forbidden as e:
        if e.api_codes[0] == 179:
            reply_to_user = reply.entities["user_mentions"][0]["screen_name"]
        else:
            raise e

    if am_i_getting_xdified(reply_to_user):
        tweet_justin(reply.id)
        return

    url = baseTwitterStatusUrl.format(reply_to_user, parent_tweet)
    media = api.media_upload(filename=get_random_image())
    api.update_status(status=mentioned_user, media_ids=[media.media_id], attachment_url=url)


def get_timeline():
    last_id = get_last_tweet()

    replies = api.search_tweets(q=userName, since_id=last_id, tweet_mode="extended")
    if len(replies) == 0:
        return

    for reply in replies:
        quote_tweet(reply)


if __name__ == "__main__":
    get_timeline()
