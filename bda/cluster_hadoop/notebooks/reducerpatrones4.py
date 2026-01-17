#!/usr/bin/env python3
import sys

codigo_actual = None
nombre_pais = None

for line in sys.stdin:
    codigo, valor = line.strip().split("\t", 1)

    if codigo != codigo_actual and codigo_actual is not None:
        nombre_pais = None

    codigo_actual = codigo

    if valor.startswith("A|"):
        nombre_pais = valor[2:]
    elif valor.startswith("B|") and nombre_pais is not None:
        print(f"{nombre_pais}\t{valor[2:]}")
