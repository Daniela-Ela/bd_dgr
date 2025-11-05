#Escribe una función que tome un diccionario y devuelva otro con las claves y valores intercambiados 
#(lo que antes eran valores ahora son claves, y viceversa).


mi_diccionario = {
    "a": 1,
    "b": 2,
    "c": 3,
}
vacio = {}
for key, value in mi_diccionario.items():
    vacio[value] = key
print(vacio)