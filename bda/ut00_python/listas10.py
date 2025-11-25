#Dada una lista de palabras, permite al usuario ingresar una palabra y cuenta cuántas veces aparece en la lista.
palabras = ["sol", "luna", "estrella", "sol", "mar", "cielo", "sol", "tierra", "mar", "nube"]

palabra_usuario = input("Escribe una palabra: ")

contador = 0

for p in palabras:
    if p.lower() == palabra_usuario.lower():  # ignora mayúsculas/minúsculas
        contador += 1

print(f"La palabra '{palabra_usuario}' aparece {contador} veces en la lista.")