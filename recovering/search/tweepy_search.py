# -*- coding: UTF-8 -*-
import tweepy
import sys

consumer_key = 'ZR2SU5TrGKQ2zCbVbyDUw'
consumer_secret = 'Rcg5Esw9z6z8JdIEfJIp4NBRzgxA3i6ISeCL1mDM'

access_token = '108874877-5N9XRZiRCTiALdKUw7sYhulzNgwFUzZgfeOw03b9'
access_token_secret = 'ogKVKjkRUie0cfP95zcT2kINVeZrbm1iyxj90dCpVwjFG'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Consigue al usuario
# user = api.get_user('jorgetuitea')
# public_tweets = api.user_timeline( user )
# for tweet in public_tweets:
#     print tweet.text

search_term = sys.argv[1]

# Archivo output:
outputFile = open('output'+search_term+'.txt', 'w')

try:
    for page in tweepy.Cursor(api.search, q=search_term, count=100, result_type="mixed", include_entities=True).pages(1):
        # Consulta el límite restante de consultas
        data = api.rate_limit_status()
        remaining = data['resources']['search']['/search/tweets']['remaining']
        print str(remaining)+' consultas restantes para Búsqueda y recuperación'
        # Fin consulta de límite
        for tweet in page:
            clean_tweet = tweet.text.encode('utf-8')
            clean_tweet = clean_tweet.replace('\n', '').replace('\r', '')
            outputFile.write(clean_tweet+'\n')
except tweepy.TweepError as e:
    print e
