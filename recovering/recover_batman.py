# -*- coding: UTF-8 -*-
# Búsqueda de tweets por término
import tweepy
import time
import sys
# import os

consumer_key = 'FvIrfi9RvEK6u4DWEn9Zq0hqK'
consumer_secret = '2pF4WiVj8Qsl11UL0CEI00Qx3ScO5g8c8GnoC73sBcY3hYPasw'

access_token = '108874877-UxDmQBYSmMl60jkiiTgn6DuwCFDud0kIyRndEhrB'
access_token_secret = 'Ob4dh7kWt5vDfRimyGxD7GsM5dJa8RxyaGhi5vWpg0n2s'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

archivo1 = sys.argv[1]
lista = open(archivo1)

outputFile = open('descriptiones_recuperadas_01.csv', 'w')

for usuario in lista:
    try:
        # Consulta el límite restante de consultas
        data = api.rate_limit_status()
        remaining = data['resources']['users']['/users/show/:id']['remaining']
        print str(remaining)+' consultas restantes para Batman'
        if remaining < 2:
            print 'Batman durmiendo zZzZzZ'
            time.sleep(60*15)
        # Fin de consulta
        user = api.get_user(usuario)
        descripcion = user.description.encode('utf-8')
        descripcion = descripcion.replace('\n', '')
        descripcion = descripcion.replace('\r', '')
        usuario = usuario.replace('\n', '').replace('\r', '')
        outputFile.write(usuario+',"'+descripcion+'"\n')
        print usuario
    except Exception, e:
        if e.message[0]['code'] == 88:
            print 'Batman durmiendo zZzZzZ'
            time.sleep(60*15)
        else:
            usuario = usuario.replace('\n', '').replace('\r', '')
            outputFile.write(usuario+',"no_description"'+'\n')
            print usuario
