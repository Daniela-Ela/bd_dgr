# **PR0404: Aplicación de patrones MapReduce**

## **Ejercicio 1: Limpieza y Transformación**

### **Patrón**

Filtrado y transformación.

### **Objetivo**

El dataset tiene años muy antiguos y valores nulos. Queremos un dataset limpio para años del siglo XXI.

### **Implementación**

**Mapper**:
- Lee línea por línea desde ``sys.stdin``.
- **Valida**: ignora cabeceras o líneas con errores de formato.
- **Filtra**: conserva solo registros donde ``year >= 2000`` y ``total_gdp > 0``.
- **Transforma**: emite solo ``Country Name``, ``Year`` y ``Total GDP``.
- **Salida**: imprime en STDOUT separado por tabuladores (``\t``).
  
**Reducer**:
- En este caso el reducer no tiene que hacer nada


```python
%%writefile mapperpatrones1.py
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


```

    Overwriting mapperpatrones1.py



```python
!cat countries_gdp_hist.csv | python3 mapperpatrones1.py |head 
```

    ARUBA	2000	1873452513.96648
    ARUBA	2001	1896456983.24022
    ARUBA	2002	1961843575.41899
    ARUBA	2003	2044111731.84358
    ARUBA	2004	2254830726.25698
    ARUBA	2005	2360017318.43575
    ARUBA	2006	2469782681.56425
    ARUBA	2007	2677641340.78212
    ARUBA	2008	2843024581.00559
    ARUBA	2009	2553793296.08939
    Traceback (most recent call last):
      File "/media/notebooks/mapperpatrones1.py", line 27, in <module>
        print(f"{country_name}\t{year}\t{total_gdp}")
    BrokenPipeError: [Errno 32] Broken pipe
    cat: write error: Broken pipe


## **Ejercicio 2: Agregación por clave**

### **Patrón**

Resumen numérico (promedio).

### **Objetivo**

Calcular el PIB promedio histórico por cada Región (Asia, Americas, Europe…).

### **Implementación**

**1. Mapper**:
- Extrae ``region_name`` y ``total_gdp``.
- Emite: ``REGION \t GDP``

**2. Reducer**:
- Hadoop envía los datos ordenados por clave, hay que ir sumando los valores y el número de ocurrencias de la clave que llevamos. Cuando cambie la clave se emite el promedio de la región y se resetean contadores.

**3. Salida esperada**:
- ``AMERICAS 650000.50``, ``EUROPE 540000.20``, etc.


```python
%%writefile mapperpatrones2.py
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
```

    Overwriting mapperpatrones2.py



```python
%%writefile reducerpatrones2.py
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
```

    Overwriting reducerpatrones2.py



```python
!cat countries_gdp_hist.csv | python3 mapperpatrones2.py | sort | python3 reducerpatrones2.py
```

    AFRICA	17415301365.06
    AMERICAS	250120768754.78
    ASIA	205913293760.72
    EUROPE	213179096872.72
    OCEANIA	32533011434.88


## **Ejercicio 3: Máximos por grupo (Filtering/Top-K)**

### **Patrón**

Top-K per Group.

### **Objetivo**

Encontrar el año de mayor variación de PIB (``gdp_variation``) para cada país.

### **Implementación**

**1. Mapper**:
- Emite: ``Country_Name \t Year,Variation`` (Concatena año y variación en el valor para no perder el dato del año).

**2. Reducer**:
- Para cada país, recorre todas las variaciones.
- Mantén en memoria solo la variación más alta encontrada hasta el momento y su año asociado.
- Al cambiar de país, emite: ``PAIS \t AÑO_RECORD (VARIACION)``


```python
%%writefile mapperpatrones3.py
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
```

    Overwriting mapperpatrones3.py



```python
%%writefile reducerpatrones3.py
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

```

    Writing reducerpatrones3.py



```python
!cat countries_gdp_hist.csv | python3 mapperpatrones3.py | sort | python3 reducerpatrones3.py
```

    AFGHANISTAN	2002 (28.60)
    ALBANIA	1995 (13.32)
    ALGERIA	1963 (34.31)
    AMERICAN SAMOA	2020 (4.41)
    ANDORRA	2022 (9.56)
    ANGOLA	2005 (15.03)
    ANTIGUA AND BARBUDA	2006 (12.71)
    ARGENTINA	1965 (10.57)
    ARMENIA	2003 (14.00)
    ARUBA	2021 (24.13)
    AUSTRALIA	1970 (7.18)
    AUSTRIA	1970 (7.12)
    AZERBAIJAN	2006 (34.50)
    BAHAMAS	1979 (26.14)
    BAHRAIN	1976 (30.48)
    BANGLADESH	1964 (10.95)
    BARBADOS	2022 (17.83)
    BELARUS	2004 (11.45)
    BELGIUM	1964 (6.96)
    BELIZE	2021 (17.75)
    BENIN	1981 (9.95)
    BERMUDA	1966 (14.36)
    BHUTAN	1987 (29.05)
    BOLIVIA (PLURINATIONAL STATE OF)	1968 (8.53)
    BOSNIA AND HERZEGOVINA	1996 (54.20)
    BOTSWANA	1972 (26.36)
    BRAZIL	1973 (13.97)
    BRUNEI DARUSSALAM	1979 (24.34)
    BULGARIA	1988 (10.94)
    BURKINA FASO	1996 (11.01)
    BURUNDI	1970 (21.33)
    CABO VERDE	1994 (19.18)
    CAMBODIA	1987 (21.53)
    CAMEROON	1978 (22.00)
    CANADA	1962 (7.43)
    CAYMAN ISLANDS	2022 (5.16)
    CENTRAL AFRICAN REPUBLIC	1984 (9.48)
    CHAD	2004 (33.63)
    CHILE	2021 (11.33)
    CHINA	1970 (19.30)
    COLOMBIA	2021 (10.80)
    COMOROS	2000 (10.85)
    CONGO	1982 (23.60)
    CONGO, DEMOCRATIC REPUBLIC OF THE	1962 (21.20)
    COSTA RICA	1992 (9.20)
    CROATIA	2021 (12.63)
    CUBA	1981 (19.69)
    CURAÇAO	2022 (6.91)
    CYPRUS	1976 (20.27)
    CZECHIA	2006 (6.62)
    CÔTE D'IVOIRE	1964 (17.61)
    DENMARK	1964 (9.27)
    DJIBOUTI	2015 (7.53)
    DOMINICA	1980 (13.38)
    DOMINICAN REPUBLIC	1970 (18.23)
    ECUADOR	1973 (13.95)
    EGYPT	1976 (13.28)
    EL SALVADOR	2021 (11.90)
    EQUATORIAL GUINEA	1997 (149.97)
    ERITREA	1994 (21.22)
    ESTONIA	1997 (13.05)
    ESWATINI	1990 (21.02)
    ETHIOPIA	1987 (13.86)
    FAROE ISLANDS	2012 (7.08)
    FIJI	2022 (19.79)
    FINLAND	1969 (9.59)
    FRANCE	1969 (7.11)
    FRENCH POLYNESIA	1974 (18.00)
    GABON	1974 (39.49)
    GAMBIA	1975 (12.39)
    GEORGIA	2007 (12.58)
    GERMANY	1969 (7.42)
    GHANA	2011 (14.05)
    GIBRALTAR	1960 (0.00)
    GREECE	1961 (13.20)
    GREENLAND	1971 (13.06)
    GRENADA	2005 (13.28)
    GUAM	2004 (6.49)
    GUATEMALA	1963 (9.54)
    GUINEA	2016 (10.82)
    GUINEA-BISSAU	1981 (18.17)
    GUYANA	2022 (63.33)
    HAITI	1995 (9.90)
    HONDURAS	2021 (12.57)
    HONG KONG	1976 (16.16)
    HUNGARY	1965 (42.41)
    ICELAND	1971 (13.06)
    INDIA	2021 (9.69)
    INDONESIA	1968 (10.92)
    IRAN (ISLAMIC REPUBLIC OF)	1982 (23.17)
    IRAQ	1990 (57.82)
    IRELAND	2015 (24.62)
    ISLE OF MAN	1986 (19.11)
    ISRAEL	1968 (16.24)
    ITALY	2021 (8.93)
    JAMAICA	1972 (18.01)
    JAPAN	1968 (12.88)
    JORDAN	1979 (20.80)
    KAZAKHSTAN	2001 (13.50)
    KENYA	1971 (22.17)
    KIRIBATI	1974 (45.30)
    KOREA (DEMOCRATIC PEOPLE'S REPUBLIC OF)	1960 (0.00)
    KOREA, REPUBLIC OF	1973 (14.90)
    KUWAIT	1992 (82.81)
    KYRGYZSTAN	1988 (13.20)
    LAO PEOPLE'S DEMOCRATIC REPUBLIC	1989 (14.19)
    LATVIA	2006 (12.83)
    LEBANON	1991 (49.45)
    LESOTHO	1973 (26.40)
    LIBERIA	1997 (106.28)
    LIBYA	2012 (86.83)
    LIECHTENSTEIN	1999 (10.41)
    LITHUANIA	2007 (11.08)
    LUXEMBOURG	1986 (9.98)
    MACAO	2023 (75.06)
    MADAGASCAR	1979 (9.85)
    MALAWI	1995 (16.73)
    MALAYSIA	1973 (11.70)
    MALDIVES	2021 (37.51)
    MALI	1985 (20.29)
    MALTA	2000 (19.68)
    MARSHALL ISLANDS	1973 (33.92)
    MAURITANIA	1964 (27.69)
    MAURITIUS	1976 (23.75)
    MEXICO	1964 (11.91)
    MICRONESIA (FEDERATED STATES OF)	1973 (33.93)
    MOLDOVA, REPUBLIC OF	2021 (13.93)
    MONACO	2021 (22.23)
    MONGOLIA	2011 (17.29)
    MONTENEGRO	2021 (13.04)
    MOROCCO	1996 (12.37)
    MOZAMBIQUE	1987 (14.70)
    MYANMAR	2003 (13.84)
    NAMIBIA	2004 (12.27)
    NAURU	2012 (25.28)
    NEPAL	1984 (9.68)
    NETHERLANDS	1965 (8.64)
    NEW CALEDONIA	1988 (34.60)
    NEW ZEALAND	1969 (10.19)
    NICARAGUA	1974 (14.19)
    NIGER	1978 (13.47)
    NIGERIA	1970 (25.01)
    NORTH MACEDONIA	2007 (6.47)
    NORTHERN MARIANA ISLANDS	2016 (29.21)
    NORWAY	1961 (6.27)
    OMAN	1965 (100447998.41)
    PAKISTAN	1970 (11.35)
    PALAU	1995 (10.90)
    PALESTINE, STATE OF	2004 (21.92)
    PANAMA	2021 (16.47)
    PAPUA NEW GUINEA	1993 (18.20)
    PARAGUAY	1978 (12.03)
    PERU	2021 (13.36)
    PHILIPPINES	1973 (8.78)
    POLAND	1995 (7.93)
    PORTUGAL	1973 (11.20)
    PUERTO RICO	1969 (9.38)
    QATAR	1997 (30.01)
    ROMANIA	2004 (10.43)
    RUSSIAN FEDERATION	2000 (10.00)
    RWANDA	1995 (35.22)
    SAINT KITTS AND NEVIS	2008 (11.32)
    SAINT LUCIA	2022 (20.39)
    SAINT MARTIN (FRENCH PART)	2019 (6.50)
    SAINT VINCENT AND THE GRENADINES	1972 (25.83)
    SAMOA	1971 (13.51)
    SAN MARINO	2021 (13.90)
    SAO TOME AND PRINCIPE	1977 (23.42)
    SAUDI ARABIA	1970 (52.59)
    SENEGAL	1976 (8.92)
    SERBIA	1997 (8.93)
    SEYCHELLES	1978 (21.15)
    SIERRA LEONE	2002 (26.52)
    SINGAPORE	2010 (14.52)
    SINT MAARTEN (DUTCH PART)	2019 (10.97)
    SLOVAKIA	2007 (10.82)
    SLOVENIA	2021 (8.39)
    SOLOMON ISLANDS	1992 (12.70)
    SOMALIA	1972 (14.88)
    SOUTH AFRICA	1964 (7.94)
    SOUTH SUDAN	2013 (13.13)
    SPAIN	1961 (11.84)
    SRI LANKA	2011 (8.67)
    SUDAN	1997 (18.31)
    SURINAME	1966 (19.20)
    SWEDEN	1964 (6.82)
    SWITZERLAND	1961 (8.11)
    SYRIAN ARAB REPUBLIC	1974 (25.80)
    TAJIKISTAN	1988 (13.90)
    TANZANIA, UNITED REPUBLIC OF	1966 (11.64)
    THAILAND	1988 (13.29)
    TIMOR-LESTE	2000 (58.08)
    TOGO	1965 (15.46)
    TONGA	2011 (6.70)
    TRINIDAD AND TOBAGO	2003 (14.44)
    TUNISIA	1972 (17.74)
    TURKEY	2021 (11.44)
    TURKMENISTAN	1990 (35.38)
    TURKS AND CAICOS ISLANDS	2015 (11.31)
    TUVALU	1986 (22.59)
    UGANDA	1995 (11.52)
    UKRAINE	2004 (11.80)
    UNITED ARAB EMIRATES	1973 (76.62)
    UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND	2021 (8.58)
    UNITED STATES OF AMERICA	1984 (7.24)
    URUGUAY	1986 (8.81)
    UZBEKISTAN	2007 (9.47)
    VANUATU	1990 (11.70)
    VENEZUELA (BOLIVARIAN REPUBLIC OF)	2004 (18.29)
    VIET NAM	1995 (9.54)
    VIRGIN ISLANDS (BRITISH)	1960 (0.00)
    VIRGIN ISLANDS (U.S.)	2007 (4.01)
    YEMEN	1992 (8.21)
    ZAMBIA	1965 (16.65)
    ZIMBABWE	1970 (22.57)


## **Ejercicio 4: Join (Reduce-Side Join)**

### **Patrón** 

Reduce-Side Join.

### **Objetivo**

Unir el dataset de PIB con un dataset auxiliar de códigos de país para obtener el nombre completo en español (simulado).

### **Implementación**

**1. Datos Auxiliares**: necesitas un fichero que relacione los códigos de los países con su respectivo nombre. Puedes utilizar este dataset disponible en Github.

**2. Estrategia**:
- Subir ambos archivos (``gdp.csv`` y ``codes.csv``) a HDFS.
- **Mapper**

Debe detectar qué archivo está leyendo. Una forma de hacerlo sería contando la cantidad de columnas del fichero. Ten cuidado, porque en un fichero el separador es el punto y coma, mientras que en el otro es la coma, así que lo que puedes hacer es:
  
  Separo por comas, si obtengo ``X`` campos es el fichero ``codes.csv``
  
  Si no, separo por punto y coma, y compruebo que el número de campos concuerda con el fichero ``gdp.csv``

Si es ``codes.csv``: Emite ``CODIGO \t A_NombreEsp`` (Tag ‘A’, que usaré en el reducer para distinguir entre uno y otro).

Si es ``gdp.csv``: Emite ``CODIGO \t B_PIB`` (Tag ‘B’).

- **Reducer**
        Recibirá todas las líneas de un mismo código juntas (ej. ``ESP``).
        Guarda el nombre en español (Tag A) en una variable.
        Cuando lleguen los datos del PIB (Tag B), imprime: ``Nombre_Español \t PIB.

**3. Ejecución**: ten en cuenta que, en este caso, el mapper recibirá dos ficheros, por lo que habría que invocarlo de la siguiente forma (observa que hay dos ``-input``):



```python
%%writefile mapperpatrones4.py
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

```

    Writing mapperpatrones4.py



```python
%%writefile reducerpatrones4.py
#!/usr/bin/env python3
import sys

codigo_actual = None
nombre_pais = None

for line in sys.stdin:
    codigo, valor = line.strip().split("\t", 1)

    if codigo != codigo_actual and codigo_actual is not None:
        nombre_pais = None

    codigo_actual = codigo

    if valor.startswith("A|"):
        nombre_pais = valor[2:]
    elif valor.startswith("B|") and nombre_pais is not None:
        print(f"{nombre_pais}\t{valor[2:]}")

```

    Writing reducerpatrones4.py



```python
!cat all.csv countries_gdp_hist.csv | python3 mapperpatrones4.py | sort | python3 reducerpatrones4.py | tail -100 
```

    Zambia	27141.0235580829
    Zambia	2719.51893299541
    Zambia	2742.8592629794002
    Zambia	27577.956471244
    Zambia	28037.2394627142
    Zambia	2811.03247293922
    Zambia	2910.98126210018
    Zambia	29163.7821404858
    Zambia	3182.81084101704
    Zambia	3273.50775387841
    Zambia	3288.3817973241503
    Zambia	3321.04845115171
    Zambia	3353.44537815126
    Zambia	3376.8066971218
    Zambia	3404.2848905306
    Zambia	3537.74194189367
    Zambia	3597.2209620001704
    Zambia	3600.63211141414
    Zambia	3656.80823264295
    Zambia	3728.87814880792
    Zambia	3806.9826788936302
    Zambia	3871.11709286676
    Zambia	3884.53085376162
    Zambia	3994.67316102649
    Zambia	4008.1264973646403
    Zambia	4094.44130121423
    Zambia	4193.85044542632
    Zambia	4303.2884797086
    Zambia	4901.86976405957
    Zambia	6221.11021945542
    Zambia	679.27972855982
    Zambia	682.359727329053
    Zambia	698.739720783607
    Zambia	704.339718545848
    Zambia	822.639671273187
    Zambia	8331.87016914977
    Zimbabwe	1052.9904
    Zimbabwe	1096.6466
    Zimbabwe	1117.6016
    Zimbabwe	1159.5117
    Zimbabwe	12041.6552
    Zimbabwe	1217.138
    Zimbabwe	1281.7495
    Zimbabwe	1311.4358
    Zimbabwe	1397.002
    Zimbabwe	14101.9203
    Zimbabwe	1479.5999
    Zimbabwe	17114.8499
    Zimbabwe	1747.9988
    Zimbabwe	1884.2063
    Zimbabwe	19091.02
    Zimbabwe	19495.5196
    Zimbabwe	19963.1206
    Zimbabwe	20548.6781
    Zimbabwe	2178.7163
    Zimbabwe	25717.409842447898
    Zimbabwe	2677.7294
    Zimbabwe	26867.936444682597
    Zimbabwe	27240.515108804902
    Zimbabwe	32789.7517363323
    Zimbabwe	3309.3536
    Zimbabwe	34156.0699180609
    Zimbabwe	35231.3678858554
    Zimbabwe	3982.1614
    Zimbabwe	4318.372
    Zimbabwe	4351.6005
    Zimbabwe	4364.3821
    Zimbabwe	4371.3007
    Zimbabwe	4415.7028
    Zimbabwe	51074.6605133715
    Zimbabwe	5177.4594
    Zimbabwe	5291.9501
    Zimbabwe	5443.8965
    Zimbabwe	5637.2593
    Zimbabwe	5727.5918
    Zimbabwe	5755.2152
    Zimbabwe	5805.5984
    Zimbabwe	6217.5237
    Zimbabwe	6342.1164
    Zimbabwe	6352.1259
    Zimbabwe	6401.9682
    Zimbabwe	6563.8133
    Zimbabwe	6678.8682
    Zimbabwe	6689.9576
    Zimbabwe	6741.2151
    Zimbabwe	6751.4722
    Zimbabwe	6777.3847
    Zimbabwe	6858.0131
    Zimbabwe	6890.675
    Zimbabwe	7111.2707
    Zimbabwe	7764.067
    Zimbabwe	7814.7841
    Zimbabwe	8011.3738
    Zimbabwe	8286.3227
    Zimbabwe	8529.5716
    Zimbabwe	8539.7007
    Zimbabwe	8553.1466
    Zimbabwe	8641.4817
    Zimbabwe	8783.8167
    Zimbabwe	9665.7933


## **Ejercicio 5: Distribución de Riqueza (Binning Pattern)**

### **Patrón**

Binning (Categorización en cubos).

### **Objetivo**

Clasificar los registros en rangos de riqueza definidos manualmente para generar un histograma. En lugar de agrupar por una columna existente (como Región), debes crear tu propia clave de agrupación basada en lógica de negocio.

Queremos saber cuántos registros de la historia corresponden a economías “Pequeñas”, “Medianas” y “Grandes” basándonos en el ``total_gdp_million``.

Las **reglas de negocio (bins)** son:

- **Economía Pequeña:** GDP < 10,000 Millones.
- **Economía Mediana:** 10,000 <= GDP < 1,000,000 Millones.
- **Economía Grande:** GDP >= 1,000,000 Millones.

### **Implementación**

1. Mapper

- Leer ``total_gdp_million``.
- Determinar la categoría según las reglas de negocio.
- **Salida**: ``CATEGORIA \t 1`` (Emitimos un 1 para contar).

2. **Reducer**

- Suma simple de los “1” recibidos por cada categoría.
- **Salida esperada**:
![imagen.png](172e3350-2c6e-4282-a1f3-d826302ee05a.png)


```python
%%writefile mapperpatrones5.py
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

```

    Writing mapperpatrones5.py



```python
%%writefile reducerpatrones5.py
#!/usr/bin/env python3
import sys

categoria_actual = None
contador = 0

for line in sys.stdin:
    categoria, valor = line.strip().split("\t")
    valor = int(valor)

    if categoria == categoria_actual:
        contador += valor
    else:
        if categoria_actual is not None:
            print(f"{categoria_actual}\t{contador}")
        categoria_actual = categoria
        contador = valor

if categoria_actual is not None:
    print(f"{categoria_actual}\t{contador}")

```

    Writing reducerpatrones5.py



```python
!cat countries_gdp_hist.csv | python3 mapperpatrones5.py | sort | python3 reducerpatrones5.py
```

    Economia Grande	423
    Economia Mediana	4777
    Economia Pequena	8560


## **Ejercicio 6: Índice invertido de países (Inverted Index Pattern)**

### **Patrón**

Inverted Index (con deduplicación).

### **Objetivo**

Generar una lista de búsqueda rápida. Dado un nivel de ingresos (``income_group``), queremos obtener la lista de todos los países únicos que pertenecen a ese grupo.

El dataset es una serie temporal. El par (``INGRESO`` ``ALTO``, ``ESPAÑA``) aparece unas 60 veces (una vez por cada año desde 1960). El reducer debe ser capaz de eliminar duplicados para no listar “España” 60 veces.

### **Implementación**

1. **Mapper**
    - Leer ``income_group`` y ``country_name``
    - **Salida**: ``INCOME_GROUP \t COUNTRY_NAME``

2. **Reducer**
    - Recibir la lista de países para un grupo.
    - Almacenar los países en una estructura que no admita duplicados (como un ``set`` de Python) mientras se itera sobre la misma clave.
    - Al cambiar de clave, unir el set en un string separado por comas.
    - **Salida esperada**:
      
      ![{470F4EFF-9110-4E9B-9841-3927B7BF1B40}.png](522b6b41-331c-4ee6-abb5-80b0e76621e6.png)


```python
%%writefile mapperpatrones6.py
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

```

    Writing mapperpatrones6.py



```python
%%writefile reducerpatrones6.py
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

```

    Writing reducerpatrones6.py



```python
!cat countries_gdp_hist.csv | python3 mapperpatrones6.py | sort | python3 reducerpatrones6.py
```

    INGRESO ALTO	AMERICAN SAMOA, ANDORRA, ANTIGUA AND BARBUDA, ARUBA, AUSTRALIA, AUSTRIA, BAHAMAS, BAHRAIN, BARBADOS, BELGIUM, BERMUDA, BRUNEI DARUSSALAM, BULGARIA, CANADA, CAYMAN ISLANDS, CHILE, CROATIA, CURAÇAO, CYPRUS, CZECHIA, DENMARK, ESTONIA, FAROE ISLANDS, FINLAND, FRANCE, FRENCH POLYNESIA, GERMANY, GIBRALTAR, GREECE, GREENLAND, GUAM, GUYANA, HONG KONG, HUNGARY, ICELAND, IRELAND, ISLE OF MAN, ISRAEL, ITALY, JAPAN, KOREA, REPUBLIC OF, KUWAIT, LATVIA, LIECHTENSTEIN, LITHUANIA, LUXEMBOURG, MACAO, MALTA, MONACO, NAURU, NETHERLANDS, NEW CALEDONIA, NEW ZEALAND, NORTHERN MARIANA ISLANDS, NORWAY, OMAN, PALAU, PANAMA, POLAND, PORTUGAL, PUERTO RICO, QATAR, ROMANIA, RUSSIAN FEDERATION, SAINT KITTS AND NEVIS, SAINT MARTIN (FRENCH PART), SAN MARINO, SAUDI ARABIA, SEYCHELLES, SINGAPORE, SINT MAARTEN (DUTCH PART), SLOVAKIA, SLOVENIA, SPAIN, SWEDEN, SWITZERLAND, TRINIDAD AND TOBAGO, TURKS AND CAICOS ISLANDS, UNITED ARAB EMIRATES, UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND, UNITED STATES OF AMERICA, URUGUAY, VIRGIN ISLANDS (BRITISH), VIRGIN ISLANDS (U.S.)
    INGRESO MEDIANO ALTO	ALBANIA, ALGERIA, ARGENTINA, ARMENIA, AZERBAIJAN, BELARUS, BELIZE, BOSNIA AND HERZEGOVINA, BOTSWANA, BRAZIL, CHINA, COLOMBIA, COSTA RICA, CUBA, DOMINICA, DOMINICAN REPUBLIC, ECUADOR, EL SALVADOR, EQUATORIAL GUINEA, FIJI, GABON, GEORGIA, GRENADA, GUATEMALA, INDONESIA, IRAN (ISLAMIC REPUBLIC OF), IRAQ, JAMAICA, KAZAKHSTAN, LIBYA, MALAYSIA, MALDIVES, MARSHALL ISLANDS, MAURITIUS, MEXICO, MOLDOVA, REPUBLIC OF, MONGOLIA, MONTENEGRO, NAMIBIA, NORTH MACEDONIA, PARAGUAY, PERU, SAINT LUCIA, SAINT VINCENT AND THE GRENADINES, SERBIA, SOUTH AFRICA, SURINAME, THAILAND, TONGA, TURKEY, TURKMENISTAN, TUVALU, UKRAINE
    NO CLASIFICADO	VENEZUELA (BOLIVARIAN REPUBLIC OF)
    PAÍSES DE INGRESO BAJO	AFGHANISTAN, BURKINA FASO, BURUNDI, CENTRAL AFRICAN REPUBLIC, CHAD, CONGO, DEMOCRATIC REPUBLIC OF THE, ERITREA, ETHIOPIA, GAMBIA, GUINEA-BISSAU, KOREA (DEMOCRATIC PEOPLE'S REPUBLIC OF), LIBERIA, MADAGASCAR, MALAWI, MALI, MOZAMBIQUE, NIGER, RWANDA, SIERRA LEONE, SOMALIA, SOUTH SUDAN, SUDAN, SYRIAN ARAB REPUBLIC, TOGO, UGANDA, YEMEN
    PAÍSES DE INGRESO MEDIANO BAJO	ANGOLA, BANGLADESH, BENIN, BHUTAN, BOLIVIA (PLURINATIONAL STATE OF), CABO VERDE, CAMBODIA, CAMEROON, COMOROS, CONGO, CÔTE D'IVOIRE, DJIBOUTI, EGYPT, ESWATINI, GHANA, GUINEA, HAITI, HONDURAS, INDIA, JORDAN, KENYA, KIRIBATI, KYRGYZSTAN, LAO PEOPLE'S DEMOCRATIC REPUBLIC, LEBANON, LESOTHO, MAURITANIA, MICRONESIA (FEDERATED STATES OF), MOROCCO, MYANMAR, NEPAL, NICARAGUA, NIGERIA, PAKISTAN, PALESTINE, STATE OF, PAPUA NEW GUINEA, PHILIPPINES, SAMOA, SAO TOME AND PRINCIPE, SENEGAL, SOLOMON ISLANDS, SRI LANKA, TAJIKISTAN, TANZANIA, UNITED REPUBLIC OF, TIMOR-LESTE, TUNISIA, UZBEKISTAN, VANUATU, VIET NAM, ZAMBIA, ZIMBABWE



```python

```
