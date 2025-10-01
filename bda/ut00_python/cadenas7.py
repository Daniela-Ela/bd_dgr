#Crea un programa que verifique si dos cadenas son anagramas. Se considera que dos palabras son anagramas si tienen las mismas letras en diferente orden, por ejemplo, lácteo y coleta.
cadena1 = input("Ingrese la primera cadena: ")
cadena2 = input("Ingrese la segunda cadena: ")
def son_anagramas(cad1, cad2):
    # Eliminar espacios y convertir a minúsculas
    cad1 = cad1.replace(" ", "").lower()
    cad2 = cad2.replace(" ", "").lower()
    
    # Ordenar los caracteres de ambas cadenas
    return sorted(cad1) == sorted(cad2)

if son_anagramas(cadena1, cadena2):
    print("Las cadenas son anagramas.")
else:
    print("Las cadenas no son anagramas.")  