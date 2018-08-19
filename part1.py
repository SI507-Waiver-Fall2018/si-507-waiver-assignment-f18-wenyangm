# these should be the only imports you need
import tweepy
import nltk
import json
import sys

# write your code here
# usage should be python3 part1.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = "KrCVbP1rUh3zZud9jy1ocqhrh"
consumer_secret = "eyR7P84wQIFiRx39mQNbBOtPQOAtJ5QIF9PpSw9fvRw0kUXw2d"
access_token = "822940557936852993-9dk3c24ws5E2r41BHxDTzu4CH22BukD"
access_token_secret = "sTfPg3xptot00AfBckVd48Onwrdpae7YYPvr0CLPu874f"

# copyright https://stackoverflow.com/questions/25588272/return-a-users-tweets-with-tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# get uesr timeline
tweets = api.user_timeline(screen_name=username, count=num_tweets, include_rts=True)

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
w_t_list = nltk.pos_tag(list(w_c.keys()))

# concatenate them to form (word, tag, count)
w_t_c = []
for w, t in w_t_list:
    w_t_c.append((w, t, w_c[w]))

# functions for finding top 5
def top5(pos='VB'):
    verbs = [x for x in w_t_c if x[1][:2] == pos]
    k = min(len(verbs), 5)
    top5 = sorted(verbs, key=lambda x: -x[2])[:k]
    return top5

top_verbs = top5('VB')
top_nouns = top5('NN')
top_adjs = top5('JJ')

# find all orginal tweets and corresponding favorite_count and retweet_count
originals = []
for tweet in tweets:
    if not tweet._json['retweeted']:
        originals.append( (tweet._json['id'], tweet._json['favorite_count'], tweet._json['retweet_count']) )

fav_count = sum([x[1] for x in originals])
rt_count = sum([x[2] for x in originals])

def printTop5(pos, top5):
    print('{}: '.format(pos), end='')
    for w,_,c in top5:
        print('{}({})'.format(w,c), end=' ')
    print()

print('USER: {}'.format(username))
print('TWEETS ANALYZED: {}'.format(num_tweets))
printTop5('VERBS', top_verbs)
printTop5('NOUNS', top_nouns)
printTop5('ADJECTIVES', top_adjs)
print('TIMES FAVORITED (ORIGINAL TWEETS ONLY): {}'.format(fav_count))
print('TIMES RETWEETED (ORIGINAL TWEETS ONLY): {}'.format(rt_count))

# finally save the nouns
with open('noun_data.csv', 'w') as f:
    s = ['Noun,Number']
    for w,_,c in top_nouns:
        s.append('{},{}'.format(w,c))
    output = '\n'.join(s)
    f.write(output)