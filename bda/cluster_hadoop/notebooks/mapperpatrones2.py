#!/usr/bin/env python3
import sys

for line in sys.stdin:
    partes = line.strip().split(";")
    if len(partes) != 10:
        continue
    if partes[0] == "country_code":
        continue

    region_name = partes[1]
    total_gdp_texto = partes[7]

    try:
        total_gdp = float(total_gdp_texto)
    except:
        continue

    print(f"{region_name}\t{total_gdp}")
