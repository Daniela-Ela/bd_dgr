#Escribe una función que reciba una cadena y cuente cuántas vocales y consonantes contiene.
cadena = input("Escribe una cadena: ")

vocales = "aeiouAEIOU"
num_vocales = 0
num_consonantes = 0

for letra in cadena:
    if letra.isalpha():  # solo cuenta letras
        if letra in vocales:
            num_vocales += 1
        else:
            num_consonantes += 1

print("Vocales:", num_vocales)
print("Consonantes:", num_consonantes)