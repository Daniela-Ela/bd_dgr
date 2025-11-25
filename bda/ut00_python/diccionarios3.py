#Escribe un programa que tome una frase y use un diccionario para contar la frecuencia de cada palabra.
frase = input("Escribe una frase: ")
palabras = frase.split()        
frecuencia = {}
for palabra in palabras:
    palabra = palabra.lower()  
    if palabra in frecuencia:
        frecuencia[palabra] += 1
    else:
        frecuencia[palabra] = 1
print("Frecuencia de palabras:")
for palabra, cuenta in frecuencia.items():
    print(f"{palabra}: {cuenta}")
