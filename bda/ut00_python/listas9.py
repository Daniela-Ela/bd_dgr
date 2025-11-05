#Dada una lista de números, escribe un programa que calcule y muestre la suma de todos sus elementos.
numeros = [5, 8, 12, 3, 7, 9, 15, 2, 10]

suma = 0

for n in numeros:
    suma += n

print("La suma de todos los números es:", suma)
