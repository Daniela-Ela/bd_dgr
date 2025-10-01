#Escribe un programa que elimine todos los caracteres no alfanuméricos (como signos de puntuación) de una cadena sin funciones.
cadena = input("Ingrese una cadena: ")
nueva_cadena = ""
for char in cadena:
    if char.isalnum() or char.isspace():
        nueva_cadena += char
print("Cadena sin caracteres no alfanuméricos:", nueva_cadena)  