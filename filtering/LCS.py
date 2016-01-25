def lcs(xstr, ystr):

    if not xstr or not ystr:
        return ""

    x, xs, y, ys = xstr[0], xstr[1:], ystr[0], ystr[1:]

    if x == y:
        return x + lcs(xs, ys)
    else:
        return max(lcs(xstr, ys), lcs(xs, ystr), key=len)

usuario = raw_input("\nPrimer termino: ")
lista = raw_input("\nSegundo termino: ")

cadena_final = (lcs(usuario, lista))

perc = (len(cadena_final) * 100) / len(lista)

print perc
