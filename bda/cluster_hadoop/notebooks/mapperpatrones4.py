#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    # ---------- CODES.CSV (coma) ----------
    if "," in line and ";" not in line:
        partes = line.split(",")
        if len(partes) < 3:
            continue

        if partes[0] == "name":
            continue

        nombre_pais = partes[0]
        codigo_alpha3 = partes[2]   #CLAVE DEL JOIN

        print(f"{codigo_alpha3}\tA|{nombre_pais}")
        continue

    # ---------- GDP.CSV (punto y coma) ----------
    if ";" in line:
        partes = line.split(";")
        if len(partes) != 10:
            continue
        if partes[0] == "country_code":
            continue

        codigo = partes[0]          # ESP, FRA...
        pib_millones = partes[8]    # total_gdp_million

        if pib_millones == "":
            continue

        print(f"{codigo}\tB|{pib_millones}")
