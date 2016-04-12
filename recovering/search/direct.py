# -*- coding: UTF-8 -*-
import os
import sys
import time
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
		print 'Archivo inexstente, creando...'
		currentFile = open(dirVerif, 'w')
	else:
		print 'Archivo encontrado, añadiendo entrada...'
		currentFile = open(dirVerif, 'a')

	# Escribe la linea en el archivo correspondiente
	currentFile.write(element)

	# Cierra el archivo
	currentFile.close()

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
