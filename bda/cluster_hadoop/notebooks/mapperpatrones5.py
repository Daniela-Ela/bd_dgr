#!/usr/bin/env python3
import sys

for line in sys.stdin:
    partes = line.strip().split(";")

    if len(partes) != 10:
        continue
    if partes[0] == "country_code":
        continue

    gdp_million_texto = partes[8]

    try:
        gdp_million = float(gdp_million_texto)
    except:
        continue

    if gdp_million < 10000:
        categoria = "Economia Pequena"
    elif 10000 <= gdp_million < 1000000:
        categoria = "Economia Mediana"
    else:
        categoria = "Economia Grande"

    print(f"{categoria}\t1")
