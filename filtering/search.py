# -*- coding: UTF-8 -*-
import os
import csv

# [0] --> id_str
# [1] --> from_user
# [2] --> text
# [3] --> created_at
# [4] --> time
# [5] --> geo_coordinates
# [6] --> user_lang
# [7] --> in_reply_to_user_id_str
# [8] --> in_reply_to_screen_name
# [9] --> from_user_id_str
# [10] --> in_reply_to_status_id_str
# [11] --> source
# [12] --> profile_image_url
# [13] --> user_followers_count
# [14] --> user_friends_count
# [15] --> status_url
# [16] --> entities_str
# [17] --> user_location
# [18] --> user_verified
# [19] --> entities_hashtags

# ======= FUNCIONES ======= #
def escribe( la_linea ):
	linea_unida = ''
	# la_linea[16].replace('"', '')
	for item in la_linea:
		if la_linea.index( item ) == 16:
			ent_temp = item.replace('"','""')
			linea_unida += ( '"'+ent_temp+'"' + ',' )
		elif la_linea.index( item ) == 2:
			ent_temp = item.replace('"','\'')
			linea_unida += ( '"'+ent_temp+'"' + ',' )
		else:
			if item.find( ',' ) > 0:
				linea_unida += ( '"'+item+'"' + ',' )
			else:
				linea_unida += ( item + ',' )
	outputFile.write( linea_unida.rstrip(',')+'\n' )

# ======= FUNCIONES END ======= #


while True:
	try:
		f = raw_input("Nombre del archivo:")
		csvfile = open('../Base/'+f+'.csv', 'r')
		break
	except IOError:
		print "Archivo no encontrado, intenta otra vez ;D"

cosa = 0
query = raw_input("¿Que buscas?:")
columna = int(raw_input("[0] --> id_str\n[1] --> from_user\n[2] --> text\n[3] --> created_at\n[4] --> time\n[5] --> geo_coordinates\n[6] --> user_lang\n[7] --> in_reply_to_user_id_str\n[8] --> in_reply_to_screen_name\n[9] --> from_user_id_str\n[10] --> in_reply_to_status_id_str\n[11] --> source\n[12] --> profile_image_url\n[13] --> user_followers_count\n[14] --> user_friends_count\n[15] --> status_url\n[16] --> entities_str\n[17] --> user_location\n[18] --> user_verified\n[19] --> entities_hashtags\n[55] --> TODAS\n\n¿En qué columna busco? (0-19):"))
# ret = int(raw_input("Incluir retweets ( 0 = NO / 1 = SI):"))

# Crea la carpeta Output y se prepara para escribir el archivo
newpath = r'Output/'
if not os.path.exists(newpath): os.makedirs(newpath)

outputFile = open( 'Output/'+ query +'_en_'+f+'.csv', 'w' )

outputFile.write( 'id_str,from_user,text,created_at,time,geo_coordinates,user_lang,in_reply_to_user_id_str,in_reply_to_screen_name,from_user_id_str,in_reply_to_status_id_str,source,profile_image_url,user_followers_count,user_friends_count,status_url,entities_str,user_location,user_verified,entities_hash'+'\n' )

# Genera archivos vacíos, hay que hacer la escritura post-verificación de existencia de elementos en la línea
# Meter resultados en un arreglo e imprimir al final
# Generating empty files is awkward, and should not be done

anita = csv.reader(csvfile, delimiter=',', quotechar='"')
if columna == 55:
	for line in anita:
		for campo in line:
			if campo.lower().find( query ) > 0:
				escribe( line )
				break
else:
	for line in anita:
		if line[ columna ].lower().find( query ) > 0:
				escribe( line )
				break



print '\nArchivo '+query+'_en_'+f+'.csv generado en carpeta Output.\nHave a Nice Day\n'

