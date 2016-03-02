# -*- coding: UTF-8 -*-
# Búsqueda de tweets por término
import tweepy
import time
import sys
# import os

consumer_key = 'kRj7XCqMl3G5wgwFUphnqNuaG'
consumer_secret = 'VuL9EJfo5BZxqI7WM9bsHwSvdV5rltfgEGjnmeciLsxFSSC3qR'

access_token = '108874877-XwDLxpFGSWWIMFtNQ6zMigUk654ZutuIXbLNQt3V'
access_token_secret = 'Qa4Q6Nj44tKUoJ7dIwaTlBmZunUtTn0dhAlABndP2bug2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

archivo1 = sys.argv[1]
lista = open(archivo1)

outputFile = open('descriptiones_recuperadas_04.csv', 'w')

for usuario in lista:
    try:
        # Consulta el límite restante de consultas
        data = api.rate_limit_status()
        remaining = data['resources']['users']['/users/show/:id']['remaining']
        print str(remaining)+' consultas restantes para Elektra'
        if remaining < 2:
            print 'Elektra durmiendo zZzZzZ'
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
            print 'Elektra durmiendo zZzZzZ'
            time.sleep(60*15)
        else:
            usuario = usuario.replace('\n', '').replace('\r', '')
            outputFile.write(usuario+',"no_description"'+'\n')
            print usuario
