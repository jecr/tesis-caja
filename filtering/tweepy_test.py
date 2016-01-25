import tweepy

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



# for follower in user.followers():
# 	print 'Usuario: '+follower.screen_name+' Bio: '+follower.description




# ===== Recupera las descripciones de los seguidores de los seguidores del usuario
# for follower in user.followers():
# 	for algo in follower.followers():
# 		print follower.screen_name+' : '+algo.description




results = api.search(q="Mice")

for result in results:
    print result.text
