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

user = api.get_user(screen_name='xdifythis')
#api.update_status(status="Hello World! I'm programming a bot!")

tweets = api.user_timeline(screen_name='AntonioMiraflo1', count=1)
print(tweets[0].text)
