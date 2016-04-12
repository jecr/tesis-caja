# -*- coding: UTF-8 -*-
import os
import sys
import json
from dateutil import parser

archivo_tweets = sys.argv[1]
directorio = sys.argv[2]

# Comprueba la existencia del directorio
if not os.path.exists(directorio):
    print directorio+' no existe, creando...'
    os.makedirs(directorio)
    print directorio+' creado'
else:
    print "El directorio ya existe"

# Abre el archivo de tweets
lista_tweets = open(archivo_tweets)

# Crea una lista vacía para almacenar las líneas del archivo
lista_py = []

# Almacena las lineas del archivo dentro de la lista
for linea in lista_tweets:
    lista_py.append(linea)

# Recorre la lista de publicaciones leyendo la fecha de creación
for element in lista_py:
    currentJson = json.loads(element)

    # Convierte y almacena la fecha en una variable temporal
    currentDate = parser.parse(currentJson['created_at'])
    currentDate = str(currentDate).split(' ')[0]

    # Si el archivo no existe, lo crea
    dirVerif = directorio+'/'+directorio+'_'+currentDate+'.txt'
    if not os.path.isfile(dirVerif):
        print directorio+'_'+currentDate+' no existe, creando...'
        currentFile = open(dirVerif, 'w')

        # Escribe la linea, luego cierra el archivo
        currentFile.write(element)
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
        if not dict_ids.has_key(currentJson['id']):

            # Escribe la linea, luego cierra el archivo
            currentFile.write(element)
        currentFile.close()
