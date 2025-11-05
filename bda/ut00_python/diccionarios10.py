#Crea una función que devuelva un diccionario que tenga como claves los números del 1 a n (siendo n un valor pasado como parámetro a la función) y como valores sus cuadrados.
def diccionario_cuadrados(n):
    cuadrados = {}
    for i in range(1, n + 1):
        cuadrados[i] = i ** 2
    return cuadrados

n = int(input("Introduce un número: "))
resultado = diccionario_cuadrados(n)

print("Diccionario de cuadrados:")
print(resultado)
