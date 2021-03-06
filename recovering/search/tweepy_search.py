# -*- coding: UTF-8 -*-
import json
import sys
import tweepy
import time

# Diccionario con claves de aplicaciones, es posible elegir una para hacer la recuperación
twitter_keys = {}

twitter_keys['alfa'] = {}
twitter_keys['alfa']['c_k'] = '6oJLTuH6Hb5bhoflAkh2EQZTf'
twitter_keys['alfa']['c_s'] = 'kQh9v4OM4plxLbpBCjkYk54iCTA3F23deJkzDXXCZvIlsmAQKN'
twitter_keys['alfa']['a_t'] = '108874877-vQqPqkK9afIZYZi89VkHqhvO0UKKO7gafKVi7pMS'
twitter_keys['alfa']['a_ts'] = 'wkpEye49yW3LuMmBGV82IsasHqprjSU2FMWc59SYe4bJJ'

twitter_keys['bravo'] = {}
twitter_keys['bravo']['c_k'] = 'X9mFEYo8smhDkSVQRPdkLDPis'
twitter_keys['bravo']['c_s'] = 'KwUWaBKxm5nslS1xBpByn5w1leYPoR5tAfuVV4JnCCPsyK077F'
twitter_keys['bravo']['a_t'] = '108874877-FqRfNGmRlsAoOX13umHyCUnLTb8BT9Fn97aL1awa'
twitter_keys['bravo']['a_ts'] = 'biUkbDcfpD5mJ2r9Cbw1V6UAh9QXipzja2am3OTEGAmWb'

twitter_keys['charlie'] = {}
twitter_keys['charlie']['c_k'] = 'QxEiwkObtSNCM2PVIdeUktCCf'
twitter_keys['charlie']['c_s'] = 'Jgb87eswqGChTISs8ISOfy6hvg77PPeF7fT3sCAy14bN03xLvx'
twitter_keys['charlie']['a_t'] = '108874877-M81jUTUDZXj6Cj86iAELibQHFCo7aZYstKucC5fY'
twitter_keys['charlie']['a_ts'] = 'OfeBrxSNvBaBr7qyUcfLPtvJopxk2pZk1S99MFla0mGdu'

# python tweepy_search.py alfa "\"hoy no circula\" OR hoynocircula OR contingenciaambiental OR \"contingencia ambiental\" OR precontingencia" hoy_no_circula.txt
# python tweepy_search.py bravo "panamapapers OR \"papeles de panama\"" panama_papers.txt

# Selección de aplicación para recuperación
app_selection = sys.argv[1]

consumer_key = twitter_keys[app_selection]['c_k']
consumer_secret = twitter_keys[app_selection]['c_s']

access_token = twitter_keys[app_selection]['a_t']
access_token_secret = twitter_keys[app_selection]['a_ts']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Argumentos de invocacón
search_term = sys.argv[2]
archivo_tweets = sys.argv[3]

# Archivo output, abre el archivo para lectura/escritura:
try:
    # Intenta abrir el archivo para lectura
    lecturaInicial = open(archivo_tweets, 'r')
except Exception, e:
    #Si falla, crea un archivo nuevo
    print "Archivo no encontrado, creando nuevo..."
    lecturaInicial = open(archivo_tweets, 'w+')

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
                print '\n'+str(len(dict_tweets))+' tweets únicos'
                print 'Alfa durmiendo zZzZzZ '+time.asctime()
                time.sleep(60)
                break
    except Exception, e:
        if  hasattr(e, 'response'):
            if e.response.status_code == 429:
                print '\n'+str(len(dict_tweets))+' tweets únicos'
                print 'Exception: Alfa durmiendo zZzZzZ '+time.asctime()
                time.sleep(60)
        else:
            print e
            pass
