#Escribe un programa que transforme una cadena de palabras separadas por espacios o guiones en formato camelCase (la primera letra de cada palabra, excepto la primera, debe ser mayúscula y no debe haber espacios ni guiones).
cadena = 'Esto es una prueba'
cadena = cadena.title()
cadena= cadena.replace(' ', '').replace('-', '')
cadena = cadena[0].lower() + cadena[1:]
print(cadena)