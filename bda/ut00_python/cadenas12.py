#Escribe una función que implemente la codificación por longitud de ejecución (RLE), que consiste en comprimir una cadena representando las secuencias consecutivas de caracteres iguales con el carácter seguido de la cantidad de repeticiones.
#Por ejemplo, la cadena aaron la reemplazaría por a2r1o1n1. Por simplicidad, puedes asumir que un carácter no se va a repetir más de 9 veces consecutivas. sin funcion
cadena = input("Ingrese una cadena: ")
if not cadena:
    print("La cadena está vacía.")
else:   
    resultado = ""
    contador = 1
    for i in range(1, len(cadena)):
        if cadena[i] == cadena[i - 1]:
            contador += 1
        else:
            resultado += cadena[i - 1] + str(contador)
            contador = 1
    resultado += cadena[-1] + str(contador)  
    print("Cadena codificada:", resultado)