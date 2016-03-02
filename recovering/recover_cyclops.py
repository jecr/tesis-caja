# -*- coding: UTF-8 -*-
# Búsqueda de tweets por término
import tweepy
import time
import sys
# import os

consumer_key = 'e2C0wlpcDF2HFRZ1isnWXvdTm'
consumer_secret = 'muqOqWH1KByuC9ARZy006P8wclAryQcUgIsa1kcEzgXuUPw1aH'

access_token = '108874877-nLkeHo0WRx6Nsz9uctXFVtt9F2oam2Y8E5UfEZjt'
access_token_secret = '7puoG65PJW1ppYgJoMQAq58p4tFbpWTnPhiMOeMnzeobI'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

archivo1 = sys.argv[1]
lista = open(archivo1)

outputFile = open('descriptiones_recuperadas_02.csv', 'w')

for usuario in lista:
    try:
        # Consulta el límite restante de consultas
        data = api.rate_limit_status()
        remaining = data['resources']['users']['/users/show/:id']['remaining']
        print str(remaining)+' consultas restantes para Cyclops'
        if remaining < 2:
            print 'Cyclops durmiendo zZzZzZ'
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
            print 'Cyclops durmiendo zZzZzZ'
            time.sleep(60*15)
        else:
            usuario = usuario.replace('\n', '').replace('\r', '')
            outputFile.write(usuario+',"no_description"'+'\n')
            print usuario
