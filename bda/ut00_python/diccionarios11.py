#Escribe un programa que tome una cadena y use un diccionario para contar cuántas veces aparece cada carácter.
str = "Especializacion de Inteligencia Artificial y Big Data"
res = {}
for char in str.lower():
    #res{char} = res{char}+1 if char in res else 1
    if char in res:
        res[char] += 1
    else:
        res[char] = 1
print(res)