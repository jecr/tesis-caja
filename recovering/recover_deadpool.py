# -*- coding: UTF-8 -*-
# Búsqueda de tweets por término
import tweepy
import time
import sys
# import os

consumer_key = 'rF1j9M05VyIYFRk8QtDvy0wWn'
consumer_secret = 'y2lYeRfxGF7pNVJ2RYHpr7m43bVwynI9YKFue8K3uW2EF54k0e'

access_token = '108874877-ObOcb8GnFh0vYlgtleluskwxVikMIU5TMooDZCOy'
access_token_secret = 'sAqrYFPDOwX8CkKXfD5nfTCeAieuAEhT8LFxYjBhAhQbd'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

archivo1 = sys.argv[1]
lista = open(archivo1)

outputFile = open('descriptiones_recuperadas_03.csv', 'w')

for usuario in lista:
    try:
        # Consulta el límite restante de consultas
        data = api.rate_limit_status()
        remaining = data['resources']['users']['/users/show/:id']['remaining']
        print str(remaining)+' consultas restantes para Deadpool'
        if remaining < 2:
            print 'Deadpool durmiendo zZzZzZ'
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
            print 'Deadpool durmiendo zZzZzZ'
            time.sleep(60*15)
        else:
            usuario = usuario.replace('\n', '').replace('\r', '')
            outputFile.write(usuario+',"no_description"'+'\n')
            print usuario
