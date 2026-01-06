#!/usr/bin/env python3
import os
import sys

for line in sys.stdin:
    line = line.strip()
     # line =  	country_code	region_name	sub_region_name	intermediate_region	country_name	income_group	year	total_gdp	total_gdp_million	gdp_variation
    lista = line.split(";")
    if len(lista) == 10: 
        country_code,region_name,sub_region_name,intermediate_region,country_name,income_group,year,total_gdp,total_gdp_million,gdp_variation = lista
        if country_code == "country_code": 
            continue
        else:  
            country_code,region_name,sub_region_name,intermediate_region,country_name,income_group,year,total_gdp,total_gdp_million,gdp_variation = lista
            year = int(year)
            total_gdp = float(total_gdp)
            if year >= 2000 and total_gdp > 0: 
                print(f"{country_name}\t{year}\t{total_gdp}")
            
    else: 
        continue
