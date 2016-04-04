# -*- coding: UTF-8 -*-
import json
import sys
import time
from dateutil import parser

# Apertura de archivo de tweets recuperados
archivo_tweets = sys.argv[1]
lista_tweets = open(archivo_tweets)

lista_py = []

for linea in lista_tweets:
	lista_py.append(linea)

unord_dates = []

for element in lista_py:
	currentJson = json.loads(element)
	currentDate = parser.parse(currentJson['created_at'])
	unord_dates.append(currentDate)

orderd_dates = sorted(unord_dates)

for fecha in orderd_dates:
	print fecha
