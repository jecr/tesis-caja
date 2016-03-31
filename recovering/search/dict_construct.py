# -*- coding: UTF-8 -*-
import json
import sys

# Apertura de archivo de tweets recuperados
archivo_tweets = sys.argv[1]
lista_tweets = open(archivo_tweets)

lista_py = []

for linea in lista_tweets:
	lista_py.append(linea)

dict_tweets = {}

for element in lista_py:
	currentJson = json.loads(element)
	currentKey = currentJson['id']
	if not dict_tweets.has_key(currentKey):
		dict_tweets[currentKey] = currentJson

print len(dict_tweets)