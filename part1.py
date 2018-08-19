# these should be the only imports you need
import tweepy
import nltk
import json
import sys

# write your code here
# usage should be python3 part1.py <username> <num_tweets>
username=sys.argv[1]
num_tweets=sys.argv[2]

consumer_key = "KrCVbP1rUh3zZud9jy1ocqhrh"
consumer_secret = "eyR7P84wQIFiRx39mQNbBOtPQOAtJ5QIF9PpSw9fvRw0kUXw2d"
access_token = "822940557936852993-9dk3c24ws5E2r41BHxDTzu4CH22BukD"
access_token_secret = "sTfPg3xptot00AfBckVd48Onwrdpae7YYPvr0CLPu874f"

# copyright https://stackoverflow.com/questions/25588272/return-a-users-tweets-with-tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# get uesr timeline
tweets = api.user_timeline(screen_name = username, count = num_tweets, include_rts = True)

# concatenate all tweet texts
all_texts = []
for tweet in tweets:
	all_texts.append(tweet._json['text'])
all_texts = ' '.join(all_texts)

# tokenize the texts
tokens = nltk.word_tokenize(all_texts)

# find valid tokens
goodPrefix = []
for num in range(97, 97+26):
    goodPrefix.append(chr(num))
for num in range(65, 65+26):
    goodPrefix.append(chr(num))
badWords = ['http', 'https', 'RT']
valids = []
for w in tokens:
    if (w[0] in goodPrefix) and (w not in badWords):
        valids.append(w)

# count word frequencies
w_c = {}
for w in valids:
	if w not in w_c:
		w_c[w] = 0
	else:
		w_c[w] += 1

# get tags
w_t = nltk.pos_tag(valids)

verbs = [x for x in w_t if x[1][:2] == 'VB']
print(verbs)