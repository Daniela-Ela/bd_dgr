#Escribe un programa que verifique si una cadena es un palíndromo (se lee igual de izquierda a derecha y de derecha a izquierda).
cadena = input("Escribe una palabra o frase: ")

texto = cadena.replace(" ", "").lower()

invertida = texto[::-1]

if texto == invertida:
    print("Es un palíndromo")
else:
    print("No es un palíndromo")