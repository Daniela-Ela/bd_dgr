#!/usr/bin/env python3
import sys

region_actual = None
suma_gdp = 0.0
contador = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    region, gdp_texto = line.split("\t")

    try:
        gdp = float(gdp_texto)
    except:
        continue

    if region == region_actual:
        suma_gdp = suma_gdp + gdp
        contador = contador + 1
    else:
        if region_actual is not None:
            promedio = suma_gdp / contador
            print(f"{region_actual}\t{promedio:.2f}")

        region_actual = region
        suma_gdp = gdp
        contador = 1

#Imprimir la última región
if region_actual is not None:
    promedio = suma_gdp / contador
    print(f"{region_actual}\t{promedio:.2f}")
