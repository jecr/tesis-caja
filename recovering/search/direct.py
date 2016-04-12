# -*- coding: UTF-8 -*-
import os
import sys
import time
import json
from dateutil import parser

archivo_tweets = sys.argv[1]
directorio = sys.argv[2]

# Abre el archivo
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

	print str(currentDate).split(' ')[0]


if not os.path.exists(directorio):
	print directorio+' no existe, creando...'
	os.makedirs(directorio)
	print directorio+' creado'
else:
	print "El directorio ya existe"

# Si el directorio existe, verificamos la existencia de archivos
# Abrir archivo
# Comprobar la existencia de carpeta
# Leer tweet por tweet, comprobar fecha, convertir, simplificar
# Comprobar la existencia de archivo (conservar la variable de existencia de carpeta)
# Si el archivo existe, cargarlo a memoria, almacenarlo en un diccionario temporal y comprobar la existencia de la clave específica
# Formato de nombre del archivo: archivo_31121989.txt
# Abrir archivo para adición de contenido
# Añadir publicación
# Cerrar archivo
