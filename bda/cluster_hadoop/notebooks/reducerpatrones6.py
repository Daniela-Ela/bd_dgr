#!/usr/bin/env python3
import sys

grupo_actual = None
paises = set()

for line in sys.stdin:
    grupo, pais = line.strip().split("\t")

    if grupo == grupo_actual:
        paises.add(pais)
    else:
        if grupo_actual is not None:
            lista = ", ".join(sorted(paises))
            print(f"{grupo_actual}\t{lista}")

        grupo_actual = grupo
        paises = set()
        paises.add(pais)

if grupo_actual is not None:
    lista = ", ".join(sorted(paises))
    print(f"{grupo_actual}\t{lista}")
