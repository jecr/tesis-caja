# -*- coding: UTF-8 -*-
# Este script da formato al texto de acuerdo al estándar de csv legible por el
# Excel de MacOS de momento descarta tuits sin interacción, pendiente de
# descartar locaciones extranjeras
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
def escribe(la_linea):
    linea_unida = ''
    # la_linea[16].replace('"', '')
    line_count = 0

    for item in la_linea:
        if line_count == 16:
            ent_temp = item.replace('"', '""')
            linea_unida += ('"'+ent_temp+'"' + ',')
        elif line_count == 2:
            ent_temp = item.replace('"', '\'')
            linea_unida += ('"'+ent_temp+'"' + ',')
        elif (line_count != 3 and line_count != 5 and line_count != 6 and
              line_count != 12 and line_count != 19):
            if item.find(',') > 0:
                linea_unida += ('"'+item+'"' + ',')
            else:
                linea_unida += (item + ',')
        line_count += 1

    outputFile.write(linea_unida.rstrip(',')+'\n')

# COINCIDENCIA


def coincide_verif(lugar, compara):
    # Lugar = lugar de la lista
    # Compara = ubicación a juzgar
    # Si la cadena A está contenida en B, otorga un 100 automático
    if compara.find(lugar) > -1:
        return 100
    else:
        cadena = lugar
        comp = compara
        coincide = ''

        start = 0
        end = 1
        needle = list(cadena)[0]
        while end < len(cadena) and start < len(cadena):
            end = 1

            while comp.find(needle) > -1:
                end += 1

                if len(coincide) < len(needle):
                    coincide = needle

                desfase = 0
                needle = ''
                for item in range(start, start + end):
                    if (desfase + start) < len(cadena):
                        needle += list(cadena)[desfase + start]
                    else:
                        needle = 'null'
                    desfase += 1

            start += 1
            if start < len(cadena):
                needle = list(cadena)[start]

        return ((len(coincide) * 100) / len(cadena))

# Recorrido de ubicaciones para la comprobación


def rec_ubicaciones(destino):
    minimo_coinc = 60
    coinc_max = 0

    for ubicacion in ubicaciones:
        la_coincidencia = coincide_verif(ubicacion.lower(), destino.lower())
        if la_coincidencia > coinc_max:
            coinc_max = la_coincidencia

    if coinc_max > minimo_coinc:
        return 'pass'
    else:
        return 'epic_fail'


# ======= FUNCIONES END ======= #


while True:
    try:
        f = raw_input("Nombre del archivo base:")
        csvfile = open('../Base/'+f+'.csv', 'r')
        csvfile_dup = open('../Base/'+f+'.csv', 'r')
        break
    except IOError:
        print "Archivo no encontrado, intenta otra vez ;D"

while True:
    try:
        u = raw_input("Nombre del archivo de ubicaciones:")
        ubicaciones_temp = open('../Listas/'+u+'.csv', 'r')
        break
    except IOError:
        print "Archivo no encontrado, intenta otra vez D:"

# Conteo de lineas en el archivo inicial, para llevar cuenta del proceso
# Puede que esto consuma mucha memoria, considerar supresión
tuits_totales = sum(1 for row in csvfile_dup)

# Esta re-asignación se hace porque al parecer sólo se puede realizar un
# recorrido de archivo por script NOTAR ESTO \(>o<)/ !!!
ubicaciones = []
for ubicacion in ubicaciones_temp:
    ubicaciones.append(ubicacion)
print '\nUbicaciones leidas'

# Crea la carpeta Output y se prepara para escribir el archivo
newpath = r'Output/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

outputFile = open('Output/filtrado_de_'+f+'.csv', 'w')

outputFile.write('id_str,from_user,text,time,in_reply_to_user_id_str,'
                 'in_reply_to_screen_name,from_user_id_str,'
                 'in_reply_to_status_id_str,source,user_followers_count,'
                 'user_friends_count,status_url,entities_str,user_location,'
                 'user_verified'+'\n')
# outputFile.write('id_str,from_user,text,created_at,time,geo_coordinates,'
#                  'user_lang,in_reply_to_user_id_str,in_reply_to_screen_name,'
#                  'from_user_id_str,in_reply_to_status_id_str,source,'
#                  'profile_image_url,user_followers_count,user_friends_count,'
#                  'status_url,entities_str,user_location,user_verified,'
#                  'entities_hash'+'\n')

# Genera archivos vacíos, hay que hacer la escritura post-verificación de
# existencia de elementos en la línea
# Meter resultados en un arreglo e imprimir al final
# Generating empty files is awkward, and should not be done

archivoInicial = csv.reader(csvfile, delimiter=',', quotechar='"')

contador_lineas = 0
avance = -1
nuevo_avance = 0
for line in archivoInicial:
    # Inicia contador de porcentaje
    nuevo_avance = (contador_lineas * 100) / tuits_totales
    if (nuevo_avance-avance) >= 1:
        avance = nuevo_avance
        print str(avance) + '%'
    contador_lineas += 1
    # Termina contador de porcentaje
    if line[0].find('id_str') < 0:
        if (line[2].find(',@ RT') > 0 or line[2].find(',"@ RT') > 0 or
           line[16].find('"user_mentions":[]') < 0 or line[7] != ''):
            # Aquí se descartan items con base en ubicación
            # Se pasan por default los vacíos
            if line[17] != '':
                if rec_ubicaciones(line[17]) == 'pass':
                    escribe(line)
            else:
                escribe(line)


print '\nArchivo filtrado_de_'+f+'.csv generado en carpeta Output.'
'\nHave a Nice Day\n'
