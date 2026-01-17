#!/usr/bin/env python3
import sys

pais_actual = ""
mejor_year = 0
mejor_variacion = -999999999  

for line in sys.stdin:
    pais, year_texto, variacion_texto = line.strip().split("\t")

    year = int(year_texto)
    variacion = float(variacion_texto)

    # Si es el primer país o ha cambiado el país
    if pais_actual != "" and pais != pais_actual:
        print(f"{pais_actual}\t{mejor_year} ({mejor_variacion:.2f})")
        mejor_variacion = -999999999  
        mejor_year = 0

    # Si esta variación es mejor que la guardada, la actualizo
    if variacion > mejor_variacion:
        mejor_variacion = variacion
        mejor_year = year

    pais_actual = pais

if pais_actual != "":
    print(f"{pais_actual}\t{mejor_year} ({mejor_variacion:.2f})")
