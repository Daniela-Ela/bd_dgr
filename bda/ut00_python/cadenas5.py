#Escribe una función que elimine los caracteres duplicados en una cadena, manteniendo solo la primera aparición de cada uno.
def eliminar_duplicados(cadena):
    resultado = ""
    for char in cadena:
        if char not in resultado:
            resultado += char
    return resultado
