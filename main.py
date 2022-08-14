import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv('API_KEY')
apiSecret = os.getenv('API_SECRET')

accessToken = os.getenv('ACCESS_TOKEN')
accessTokenSecret = os.getenv('ACCESS_TOKEN_SECRET')

userName = os.getenv('USER_NAME')
lastIdFile = os.getenv('LAST_ID_FILE')

auth = tweepy.OAuth1UserHandler(apiKey, apiSecret, accessToken, accessTokenSecret)

api = tweepy.API(auth)


def get_last_tweet(file):
    f = open(file, 'r')
    last_id = int(f.read().strip())
    f.close()
    return last_id


def put_last_tweet(file, last_id):
    f = open(file, 'w')
    f.write(str(last_id))
    f.close()
    return


def quote_tweet(tweet_id):
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    url = "https://twitter.com/{}/status/{}".format(tweet.author.screen_name, tweet_id)
    api.update_status("XD", attachment_url=url)


def get_timeline(file=lastIdFile):
    last_id = get_last_tweet(file)

    replies = api.search_tweets(q=userName, since_id=last_id, tweet_mode='extended')
    if len(replies) == 0:
        return

    new_id = 1558482514758467586

    for reply in reversed(replies):
        new_id = reply.id
        parent_tweet_id = reply.in_reply_to_status_id
        parent_tweet = api.get_status(parent_tweet_id, tweet_mode='extended')
        print(parent_tweet.full_text)
        quote_tweet(parent_tweet_id)

    put_last_tweet(file, new_id)


if __name__ == '__main__':
    get_timeline()
