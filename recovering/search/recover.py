# -*- coding: UTF-8 -*-
from dateutil import parser
import json
import os
import sys
import time
import tweepy

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
app_selection = sys.argv[1]  # Claves de aplicación
search_query = sys.argv[2]  # Término(s) de búsqueda
projectTweets = sys.argv[3]  # Nombre del proyecto

consumer_key = twitter_keys[app_selection]['c_k']
consumer_secret = twitter_keys[app_selection]['c_s']

access_token = twitter_keys[app_selection]['a_t']
access_token_secret = twitter_keys[app_selection]['a_ts']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Comprueba la existencia del directorio
if not os.path.exists(projectTweets):
    print projectTweets+' no existe, creando...'
    os.makedirs(projectTweets)
    print projectTweets+' creado'
else:
    print "El directorio ya existe"

while 1 > 0:
    try:
        for page in tweepy.Cursor(api.search, q=search_query, lang="es", count=100, include_entities=True).pages(100):
            # Procesamiento de tweets
            for tweet in page:
                cleanTweet = json.dumps(tweet._json)
                jsondTweet = json.loads(cleanTweet)

                # Convierte y almacena la fecha en una variable temporal
                currentDate = parser.parse(jsondTweet['created_at'])
                currentDate = str(currentDate).split(' ')[0]

                # Si el archivo no existe, lo crea
                dirVerif = projectTweets+'/'+projectTweets+'_'+currentDate+'.txt'
                if not os.path.isfile(dirVerif):
                    print projectTweets+'_'+currentDate+' no existe, creando...'
                    currentFile = open(dirVerif, 'w')

                    # Escribe la linea, luego cierra el archivo
                    currentFile.write(cleanTweet)
                    currentFile.write('\n')
                    currentFile.close()
                else:

                    # Si el tweet no está en el archivo, escribe la linea
                    currentFile = open(dirVerif, 'r+')

                    # Crea el diccionario de ID's del archivo
                    dict_ids = {}
                    for linea in currentFile:
                        currJsonIn = json.loads(linea)
                        dict_ids[currJsonIn['id']] = ''

                    # Comprueba la existencia del ID
                    if not dict_ids.has_key(jsondTweet['id']):

                        # Escribe la linea, luego cierra el archivo
                        currentFile.write(cleanTweet)
                        currentFile.write('\n')
                    currentFile.close()

            # Consulta el límite restante de consultas
            data = api.rate_limit_status()
            remaining = data['resources']['search']['/search/tweets']['remaining']
            print str(remaining)+' consultas restantes para Búsqueda y recuperación'
            # Fin consulta de límite
            if remaining < 2:
                print app_selection+' durmiendo zZzZzZ '+time.asctime()
                time.sleep(60)
                break
    except Exception, e:
        if hasattr(e, 'response'):
            if e.response.status_code == 429:
                print 'Exception: '+app_selection+' durmiendo zZzZzZ '+time.asctime()
                time.sleep(60)
        else:
            print e
            pass
