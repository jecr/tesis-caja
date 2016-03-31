# -*- coding: UTF-8 -*-
import json
import sys
import tweepy
import time

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
archivo_tweets = sys.argv[2]

# Archivo output, abre el archivo para lectura/escritura:
lecturaInicial = open(archivo_tweets, 'r')

# Crea una lista para almacenar las lineas del archivo
lista_py = []

for linea in lecturaInicial:
    lista_py.append(linea)

# Crea un diccionario vacío para almacenar tweets
dict_tweets = {}

# Vacía el documento para eliminar viejos tuits duplicados
lecturaInicial.close()
archivoEscritura = open(archivo_tweets, 'w')

# Itera la lista para encontrar duplicados (Esto no será necesario con búsquedas frescas)
for element in lista_py:
    currentJson = json.loads(element)
    currentKey = currentJson['id']
    if not dict_tweets.has_key(currentKey):
        dict_tweets[currentKey] = currentJson
        archivoEscritura.write(element)

# Imprime el tamaño del diccionario
print str(len(dict_tweets))+' tweets únicos'

while 1 > 0:
    try:
        for page in tweepy.Cursor(api.search, q=search_term, lang="es", count=100, include_entities=True).pages(100):
            # Procesamiento de tweets
            for tweet in page:
                cleanTweet = json.dumps(tweet._json)
                jsondTweet = json.loads(cleanTweet)
                jsondId = jsondTweet['id']
                if not dict_tweets.has_key(jsondId):
                    dict_tweets[jsondId] = jsondTweet
                    archivoEscritura.write(cleanTweet)
                    archivoEscritura.write('\n')
            # Fin de procesamiento de tweets
            # Consulta el límite restante de consultas
            data = api.rate_limit_status()
            remaining = data['resources']['search']['/search/tweets']['remaining']
            print str(remaining)+' consultas restantes para Búsqueda y recuperación'
            # Fin consulta de límite
            if remaining < 2:
                print str(len(dict_tweets))+' tweets únicos'
                print 'Recuperación durmiendo zZzZzZ '+time.asctime()
                time.sleep(60)
                break
    except Exception, e:
        if  hasattr(e, 'response'):
            if e.response.status_code == 429:
                print str(len(dict_tweets))+' tweets únicos'
                print 'Exception: Recuperación durmiendo zZzZzZ '+time.asctime()
                time.sleep(60)
        else:
            print e
            pass
