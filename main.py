import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv('API_KEY')
apiSecret = os.getenv('API_SECRET')

accessToken = os.getenv('ACCESS_TOKEN')
accessTokenSecret = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuth1UserHandler(apiKey, apiSecret, accessToken, accessTokenSecret)

api = tweepy.API(auth)

def getLastTweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId

def putLastTweet(file, lastId):
    f = open(file, 'w')
    f.write(str(lastId))
    f.close()
    return

def answerTweets(file='lastId.txt'):
    lastId = getLastTweet(file)

    mentions = api.mentions_timeline(since_id=lastId, tweet_mode='extended')
    if len(mentions) == 0:
        return

    new_id = 1558482514758467586

    for mention in reversed(mentions):
        newId = mention.id
        print(mention.full_text)

    putLastTweet(file, newId)

if __name__ == '__main__':
    answerTweets()

# user = api.get_user(screen_name='xdifythis')
# #api.update_status(status="Hello World! I'm programming a bot!")
#
# tweets = api.user_timeline(screen_name='AntonioMiraflo1', count=1)
# print(tweets[0].text)
