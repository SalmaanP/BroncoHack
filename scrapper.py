import tweepy
from pymongo import MongoClient
import requests
import time
import re
import string
import secret
import classify

client = MongoClient('mongodb://localhost')
db = client['bronco']
model, vectorizer = classify.train()

def getTweets():
    auth = tweepy.OAuthHandler(secret.app_key, secret.app_secret)
    auth.set_access_token(secret.access_key,
                          secret.access_secret)

    api = tweepy.API(auth)
    california = [-124.482003, 32.528832, -114.131211, 42.0095169]

    class StreamListener(tweepy.StreamListener):
        def on_status(self, status):
            if status.retweeted and 'RT @' not in status.text:
                return
            else:
                cleaned_tweet = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                       " ", status.text)
                cleaned_tweet = " ".join(filter(lambda x: x[0] != '@', cleaned_tweet.split()))
                cleaned_tweet = cleaned_tweet.translate({ord(k): None for k in string.digits})
                cleaned_tweet = cleaned_tweet.translate({ord(k): None for k in string.punctuation})
                cleaned_tweet = cleaned_tweet.strip().lower()

                obj = {"text": status.text, "cleaned_tweet": cleaned_tweet, "id": status.id,
                       "authorID": status.author.id, "handle": status.author.screen_name,
                       "createdTime": status.created_at, "coordinates": status.coordinates}
                db['tweets'].insert_one(obj)

                prediction = classify.predict(model, vectorizer, cleaned_tweet)

                if prediction[0] == 1 and status.author.screen_name == 'maitray_shah':
                    reply = 'Hi @'+status.author.screen_name+', Sorry to hear you had to go through that. Iffy can ' \
                                                             'help you in filing a report. Click on this ' \
                                                             'http://iffybot.surge.sh/ '
                    api.update_status(reply, status.id)

                print status.text, prediction

        def on_error(self, status_code):
            print status_code
            if status_code == 420:
                return False

    stream_listener = StreamListener()

    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    stream.filter(track=["food poisoning", "#foodpoisoning", "foodpoisoning"])


while True:
    try:
        getTweets()
    except requests.exceptions.ConnectionError:
        print 'network error'
        time.sleep(60)
        continue

    except KeyboardInterrupt:
        break

    except Exception as E:
        print E
        break
