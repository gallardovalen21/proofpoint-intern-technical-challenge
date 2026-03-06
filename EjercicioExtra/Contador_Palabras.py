from collections import Counter
archivo_texto= "./textoPrueba.txt"


def limpiar_y_contar_palabras(texto):
    texto_limpio = ""
    for caracter in texto:
        if caracter.isalpha() or caracter.isspace():
            texto_limpio += caracter.lower()
        else:
            texto_limpio += " "

    palabras = texto_limpio.split()
    return Counter(palabras).most_common()


if __name__ == '__main__':
    with open(archivo_texto, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    contador_palabras = limpiar_y_contar_palabras(contenido)
    diez_frecuentes = contador_palabras[:10]
    for palabra, frecuencia in diez_frecuentes:
        print(f"{palabra}: {frecuencia}")
