#!/usr/bin/env python3
import sys

categoria_actual = None
contador = 0

for line in sys.stdin:
    categoria, valor = line.strip().split("\t")
    valor = int(valor)

    if categoria == categoria_actual:
        contador += valor
    else:
        if categoria_actual is not None:
            print(f"{categoria_actual}\t{contador}")
        categoria_actual = categoria
        contador = valor

if categoria_actual is not None:
    print(f"{categoria_actual}\t{contador}")
