#!/usr/bin/python 
# -*- coding: utf-8 -*- 
# Aarón Ramírez De la Cruz 
# Enero, 2016 

from __future__ import division 
import pandas as pd 
import argparse 
import codecs  
import re 
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

# Tamaño de ngrama para comparar cadenas de caracteres 
NGRAM_SIZE = 3 
SIMILARITY_THRESHOLD = 0.5
DICT_LOCATIONS = dict() 

def add_item(D, key, location):
    """
        D (dict): diccionario con las palabras 
        key (str): caracter inicial de 'location' 
        location (str): nombre del lugar (aka, línea del archivo de lugares) 

        return D (dict): diccionario actualizado 
    """
    # Si ya existe la letra inicial 'key' y no existe 'location' en la lista 
    if D.has_key(key):
        if location not in D[key]: 
            D[key].append(location) 
    else: 
        D.update({key:[location]})

    return D 

def preprocess(location):
    """
        Todas las palabras son preprocesadas: se convierte a minúsculas, 
        se eliminan acentos, 'ñ', espacios y signos de puntuación. 
    """
    location = location.lower() 
    # Útil para reemplazar letras con acento 
    reemplazo = {
                'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u',
                'ü':'u', '@': '', 
                'ñ':'n'} 
    regex = re.compile("(%s)" % "|".join(map(re.escape,reemplazo.keys())))
    location = location.lower()
    # Reemplaza los caracteres que aparecen como signo de
    # interrogación en el archivo CSV. 
    location = re.sub(r'[\xa0|\xc6]', 'a', location) 
    location = re.sub(r'[\x82|\x8a]', 'e', location) 
    location = re.sub(r'\xa1', 'i', location) 
    location = re.sub(r'\xa2', 'o', location) 
    location = re.sub(r'\xa3', 'u', location) 
    location = re.sub(r'[\x9a|\xc0]', '.', location) 
    location = re.sub(r'\xa4', 'n', location) 

    new_location = regex.sub(lambda x: str(reemplazo[x.string[x.start() 
                                  :x.end()]]), location.encode('UTF-8','strict')) 
    new_location = re.sub(r'[^\w|\d]', '', new_location) 

    return new_location 

def locations_as_dict(locations_file):
    """
        Almacena los lugares de 'locations_file' en un diccionario Python. 
        El formato es: 
          i ['iztacalco', 'iztapalapa', ...] 
          h ['huehuetoca', 'hueypoxtla', ...] 
          n ['naucalpandejuarez', 'nextlalpan', ...] 
    """ 
    locations = list() 
    dict_locations = dict() 

    # Abre  archivo para lectura 
    locations = codecs.open(locations_file, mode='r', encoding="utf-8").read().splitlines() 

    for line in locations: 
        location = preprocess(line)

        # La llave del diccionario será la primera letra 
        key = location[0] 
        dict_locations = add_item(dict_locations, key, location) 

    return dict_locations 

def similarity(s1, s2): 
    """
        Cálculo de la similitud Jaccard aplicada a 
        dos conjuntos de ngramas de caracteres. 
    """
    ngrams1 = build_ngrams(s1)
    ngrams2 = build_ngrams(s2) 

    #print ngrams1
    #print ngrams2 

    #print ngrams1.intersection(ngrams2)
    #print ngrams1.union(ngrams2)
    return len(ngrams1.intersection(ngrams2)) / len(ngrams1.union(ngrams2))

def build_ngrams(s):
    """
        Genera la lista de secuencia de tamaño 'NGRAM_SIZE' 
        caracteres para comparar cadenas. 

        return ngrams (set): conjunto de ngramas de caracteres.  
    """
    if len(s) <= NGRAM_SIZE: return set([s]) 

    str_len = len(s) 
    ngrams = list() 

    for i in xrange(str_len): 
        if i+NGRAM_SIZE < str_len+1:
            ngrams.append(s[i:i+NGRAM_SIZE])
            i += 1 
        else: 
            return set(ngrams) 

def isFromMX(user_location):
    # Letra inicial de la ubicación del usuario 
    ul_key = user_location[0] 

    if DICT_LOCATIONS.has_key(ul_key): 
        # Recupera los lugares posibles 
        locations = DICT_LOCATIONS[ul_key] 
        for l in locations: 
            sim = similarity(l, user_location) 
            print l, user_location, sim 
            if sim >= SIMILARITY_THRESHOLD: 
                return True 

    return False 


def verify_place(matrix_tweets): 
    user_location = str() 

    for i in xrange(len(matrix_tweets)): 
        user_location = matrix_tweets.iloc[i][16] 
        # Una celda vacía en CSV es NaN de tipo float 
        if type(user_location) is not float:
            # Limpia el contenido, en términos de los elementos 
            # del diccionario de lugares 
            user_location = preprocess(user_location) 

            if isFromMX(user_location): 
                print "        ES DE MÉXICO:", user_location 
                #print matrix_tweets.iloc[i] 
            else:
                print "NO ES DE MÉXICO:", user_location 
                #print matrix_tweets.iloc[i] 

def main():
    #print similarity("sanluispotosi", "sanluispotos") 
    #exit() 

    ap = argparse.ArgumentParser(sys.argv[0]) 
    ap.add_argument("csv_file", default=None, type=str, 
        action="store", help="Archivo CSV de tweets") 

    ap.add_argument("locations_file", default=None, type=str, 
        action="store", help="Listado de ubicaciones") 

    args = ap.parse_args() 

    # El archivo CSV es almacenado en un DataFrame para 
    # manipular fácilmente el contenido 
    matrix_tweets = pd.DataFrame.from_csv(args.csv_file) 

    # Diccionario de lugares 
    D = dict() 
    D = locations_as_dict(args.locations_file)
    global DICT_LOCATIONS 
    DICT_LOCATIONS = D 

    verify_place(matrix_tweets) 

if __name__ == '__main__':
    main()

"""
monterrey: [rey, err, rre, mon, ter, nte, ont]
monterreynewlion: [rey, err, ewl, yne, rre, lio, eyn, wli, ion, mon, new, ter, nte, ont]

intersección: [rey, err, rre, mon, ter, nte, ont] (longitud = 7) 
unión: [rre, ion, mon, ter, nte, ont, rey, err, ewl, yne, lio, eyn, wli, new] (longitud = 14) 

similitud = 7 / 14 = 0.5 

"""
