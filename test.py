import os
import re
import json

import tweepy
import requests

from word_model import WordModel

TWITTER_KEY = os.environ["TWITTER_KEY"]
TWITTER_SECRET = os.environ["TWITTER_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]
CORTICAL_API_KEY = os.environ["CORTICAL_API_KEY"]


def cleanText(text):
  out = text.encode('utf-8')
  out = re.sub(r'@([A-Za-z0-9_]+)', '', out)
  out = re.sub(r'^RT : ', '', out)
  out = re.sub(r'https?:\/\/.*[\r\n]*', '', out)
  return out


def termToBitmap(term):
  url = "http://api.cortical.io:80/rest/text?retinaName=en_associative"
  headers = {
    "Content-Type": "application/json",
    "api_key": CORTICAL_API_KEY
  }
  response = requests.post(url,
                           headers=headers,
                           data=term)
  return json.loads(response.content).pop()

def fingerprintToTerm(fingerprint):
  url = "http://api.cortical.io:80/rest/expressions/similarTerms?retinaName=en_associative"
  headers = {
    "Content-Type": "application/json",
    "api_key": CORTICAL_API_KEY
  }
  response = requests.post(url,
                           headers=headers,
                           data=json.dumps(fingerprint))
  return json.loads(response.content)


auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
model = WordModel()

api = tweepy.API(auth)

public_tweets = api.user_timeline("rhyolight", count=100)
# print type(public_tweets)
for tweet in public_tweets:
  # print tweet.text
  cleanTweet = cleanText(tweet.text)
  print cleanTweet
  sdr = termToBitmap(cleanTweet)
  # print sdr
  terms = fingerprintToTerm(sdr)
  print '\tclosest term: %s' % terms[0]['term']


