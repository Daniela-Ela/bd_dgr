#Escribe un programa que tome dos diccionarios de productos y precios, y combine los productos comunes sumando sus precios, sin duplicar los elementos únicos.
a = {
    "naranjas": 1.20,
    "manzanas": 2.50,
    "platanos": 3.10
}

b = {
    "melon": 4.20,
    "naranjas": 1.90
}

out = a
for k, v in b.items():
    if k in out:
        out[k] += v
    else:
        out[k] = v
print(out)
