#!/usr/bin/env python3
import os
import sys

for line in sys.stdin:
    partes = line.split(";")

    #Validar
    if len(partes) != 10:
        continue
    if partes[0] == "country_code":
        continue

    country_name = partes[4]
    year_texto = partes[6]
    total_gdp_texto = partes[7]

    #Transformar
    try:
        year = int(year_texto)
        total_gdp = float(total_gdp_texto)
    except:
        continue

    #Filtro y salida
    if year >= 2000 and total_gdp > 0:
        print(f"{country_name}\t{year}\t{total_gdp}")

