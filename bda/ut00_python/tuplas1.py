#Crea un diccionario de frutas y precios. 
#Permite al usuario ingresar el nombre de una fruta y muestra su precio si existe en el diccionario, o un mensaje de que no está disponible en caso contrario.
frutas = {"manzana": 1.5, "banana": 0.75, "cereza": 2.0}
nombre = input("Ingrese el nombre de la fruta: ")
if nombre in frutas:
    print(f"El precio de la {nombre} es ${frutas[nombre]}")
else:
    print(f"La {nombre} no está disponible.")