#!/usr/bin/env python3
import sys

for line in sys.stdin:
    partes = line.strip().split(";")

    if len(partes) != 10:
        continue
    if partes[0] == "country_code":
        continue

    country_name = partes[4]
    income_group = partes[5]

    print(f"{income_group}\t{country_name}")
