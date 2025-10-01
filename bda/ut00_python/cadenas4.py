#Crea una función que cuente cuántas palabras hay en una cadena, suponiendo que las palabras están separadas por espacios.
def contar_palabras(cadena):
    palabras = cadena.split()
    return len(palabras)
cadena = "Hola, ¿cómo estás hoy?"
print(contar_palabras(cadena)) 