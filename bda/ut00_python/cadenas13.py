#Crea una función que decodifique una cadena que ha sido comprimida usando el método RLE.
cadena = input("Ingrese una cadena codificada: ")
resultado = ""
i = 0
while i < len(cadena):
    char = cadena[i]
    i += 1
    count = 0
    while i < len(cadena) and cadena[i].isdigit():
        count = count * 10 + int(cadena[i])
        i += 1
    resultado += char * count
print("Cadena decodificada:", resultado)