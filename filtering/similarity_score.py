# -*- coding: cp1252 -*-
cadena = 'oaxaca'
comp = 'oaxaccra'
coincide = ''
minimo_coinc = 85

if cadena == comp:
    print 'OK'
else:
    start = 0
    end = 1
    needle = list(cadena)[0]
    while end < len(cadena) and start < len(cadena):
        print '\nAvanza caracter'
        end = 1

        while comp.find(needle) > -1:
            end += 1;

            print 'Needle found: '+needle
            if len(coincide) < len(needle):
                coincide = needle
                
            desfase = 0
            needle = ''
            for item in range(start,start + end):
                if (desfase + start) < len(cadena):
                    needle += list(cadena)[desfase + start]
                else:
                    needle = 'null'
                desfase += 1
            #print 'Needle update: '+needle

        start += 1
        if start < len(cadena):
            needle = list(cadena)[start]
        
print '\nMáxima cadena coincidente: '+coincide
print 'Porcentaje de coincidencia: '+str((len(coincide) * 100) / len(cadena))

if ( (len(coincide) * 100) / len(cadena) ) > 84:
    print 'PASA'
else:
    print 'NO PASA'
