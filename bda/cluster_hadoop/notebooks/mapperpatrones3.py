#!/usr/bin/env python3
import sys

for line in sys.stdin:
    partes = line.strip().split(";")
    if len(partes) != 10:
        continue
    if partes[0] == "country_code":
        continue

    pais = partes[4]
    year_texto = partes[6]
    variacion_texto = partes[9]

    try:
        year = int(year_texto)
        variacion = float(variacion_texto)
    except:
        continue

    print(f"{pais}\t{year}\t{variacion}")
