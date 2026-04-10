# **PR0601. Capa bronce en Amazon AWS**

## **1. Contexto**

La Secretaría de Estado de Turismo quiere desarrollar un sistema de inteligencia de datos para optimizar la gestión de las playas españolas. Para ello, necesitan centralizar en un **Data Lake en AWS (Capa Bronce)** dos fuentes de información críticas:
1. **Catálogo Nacional de Playas**: un conjunto de datos detallado con servicios, accesibilidad y características físicas.
2. **Predicción Meteorológica**: datos en tiempo real para las zonas costeras (fuente AEMET).

Tu misión es automatizar la ingesta de estos datos hacia **Amazon S3** utilizando Python.

## **2. Objetivos de la práctica**

- **Consumo de API**: gestionar la autenticación y descarga de archivos JSON desde AEMET OpenData.
- **Gestión de datos maestros**: procesar un conjunto de datos complejo en formato CSV sobre la infraestructura de las playas.
- **Arquitectura Cloud**: implementar una estructura de almacenamiento profesional y escalable en S3.
- **Seguridad**: administra secretos y claves de acceso mediante variables de entorno.

## **3. Fuentes de datos**

### **A. Catálogo de playas (CSV)**
Se proporciona un archivo con información exhaustiva de las playas. También lo puedes descargar del Portal de Datos Abiertos de ESRI .

Los campos clave para futuras analíticas son:

- ``Nombre``, ``Provincia``y ``Término_M``(Municipio).
- **Servicios**: ``Duchas``, ``Aseos``, ``Acceso_dis``, ``Bandera_az``.
- **Ubicación**: ``Latitud``, ``Longitud`` y `las coordenadas ``X``, ``Y``.
- **Estado**: ``Grado_ocup`` y ``Grado_urba``.

### **B. API AEMET OpenData (API REST)**
- **Servicio**: predicción para playas (específicamente el endpoint de predicción diaria).
- **Requisito**: obtener el JSON de predicción para las provincias presentes en el CSV.
- **Nota técnica**: el alumno deberá manejar el flujo de la API (la API de AEMET devuelve un JSON con una URL, de la cual se descarga el dato final).

## **4. Requerimientos técnicos**

### **Fase 1: Estructura de la Capa Bronce en S3**

Debes crear un bucket y organizar los datos siguiendo un esquema de **particionamiento y versionado**:
- ``bronce/catalogos/guia_playas/v1/playas.csv``
- ``bronce/meteorologia/prediccion_playas/year=YYYY/month=MM/day=DD/``

### **Fase 2: Desarrollo del ingestor (Python)**

Desarrolla un script modular que realice lo siguiente:
1. **Módulo de carga local**: leer el CSV de playas y subirlo a S3 asegurando que el nombre del archivo incluya el origen de los datos.
2. **Módulo API AEMET**: conectar con la API, extraer la predicción del día y guardarla directamente en S3 como un archivo JSON.
3. **Trazabilidad**: cada archivo subido debe contener metadatos o un nombre que permita saber en qué fecha exacta se realizó la ingesta.


```python
import boto3
import requests
import json
import pandas as pd
from datetime import datetime
```


```python
try:
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    print("¡Conexión exitosa!")
    print(f"Tienes {len(buckets['Buckets'])} buckets en tu cuenta.")
except Exception as e:
    print("Error de conexión. Revisa tus credenciales.")
    print(e)
```

    ¡Conexión exitosa!
    Tienes 1 buckets en tu cuenta.



```python
s3 = boto3.client("s3")

bucket = "bronce1"
key = "catalogos/guia_playas/v1/playas.csv" 
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYWZhZDUyMjM5QG5hemlzYXQuY29tIiwianRpIjoiNDJlNjc3NGItM2YwMS00MTRhLWJjOGMtODMxM2EzMjAyYTA0IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NzU1ODgyNDIsInVzZXJJZCI6IjQyZTY3NzRiLTNmMDEtNDE0YS1iYzhjLTgzMTNhMzIwMmEwNCIsInJvbGUiOiIifQ.h5ou35hc2ocGQQeEZjU3Z8E4AHc0t7lQKQ3PGORYO5U"
```


```python
obj = s3.get_object(Bucket=bucket, Key=key)

data = pd.read_csv(obj["Body"])

print(data.head())
```

                 X             Y  OBJECTID            Comunidad_  \
    0 -543984.9557  4.370555e+06         1             Andalucía   
    1 -529891.9081  4.367771e+06         2             Andalucía   
    2 -524448.3850  4.367937e+06         3             Andalucía   
    3 -517145.8264  4.370638e+06         4             Andalucía   
    4   -4975.9812  4.664878e+06         5  Comunitat Valenciana   
    
              Provincia Isla  Código_IN Término_M              Web_munici  \
    0            Málaga           29069  Marbella  http://www.marbella.es   
    1            Málaga           29069  Marbella  http://www.marbella.es   
    2            Málaga           29070     Mijas     http://www.mijas.es   
    3            Málaga           29070     Mijas     http://www.mijas.es   
    4  Alicante/Alacant            3018     Altea     http://www.altea.es   
    
       Identifica  ...                           Dirección  Teléfono_ Distancia1  \
    0       316.0  ...            A-7 Km. 186,7 (Marbella)  951976669      6 km.   
    1       318.0  ...            A-7 Km. 186,7 (Marbella)  951976669      7 km.   
    2       330.0  ...            A-7 Km. 186,7 (Marbella)  951976669     10 km.   
    3    402904.0  ...            A-7 Km. 186,7 (Marbella)  951976669     18 km.   
    4    450301.0  ...  Doctor Ramón y Cajal, 7 (Benidorm)  966878787     11 km.   
    
                  Composici  Fachada_Li Espacio_pr  \
    0                 Arena      Urbana         No   
    1         Arena / Grava      Urbana         No   
    2  Arena / Roca / Grava      Urbana         Sí   
    3          Arena / Roca  Semiurbana         Sí   
    4         Bolos / Grava      Urbana         No   
    
                                              Espacio__1 Coordena_4 Coordena_5  \
    0                                                       -4.8867    36.5066   
    1                                                       -4.7601    36.4865   
    2  Zona de Especial Conservación Calahonda (ES617...    -4.7112    36.4877   
    3  Zona de Especial Conservación Calahonda (ES617...    -4.6456    36.5072   
    4                                                       -0.0447    38.6024   
    
                                              URL_MAGRAM  
    0  https://sig.miteco.gob.es/93/ClienteWS/Guia-Pl...  
    1  https://sig.miteco.gob.es/93/ClienteWS/Guia-Pl...  
    2  https://sig.miteco.gob.es/93/ClienteWS/Guia-Pl...  
    3  https://sig.miteco.gob.es/93/ClienteWS/Guia-Pl...  
    4  https://sig.miteco.gob.es/93/ClienteWS/Guia-Pl...  
    
    [5 rows x 80 columns]



```python
df_codigos = pd.read_csv("Playas_codigos.csv", sep=";", encoding="latin1")
df_codigos.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID_PLAYA</th>
      <th>NOMBRE_PLAYA</th>
      <th>ID_PROVINCIA</th>
      <th>NOMBRE_PROVINCIA</th>
      <th>ID_MUNICIPIO</th>
      <th>NOMBRE_MUNICIPIO</th>
      <th>LATITUD</th>
      <th>LONGITUD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>301101</td>
      <td>Raco de l'Albir</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3011</td>
      <td>l'Alfàs del Pi</td>
      <td>38º 34' 31"</td>
      <td>-00º 03' 52"</td>
    </tr>
    <tr>
      <th>1</th>
      <td>301401</td>
      <td>Sant Joan / San Juan</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3014</td>
      <td>Alicante/Alacant</td>
      <td>38º 22' 48"</td>
      <td>-00º 24' 32"</td>
    </tr>
    <tr>
      <th>2</th>
      <td>301408</td>
      <td>El Postiguet</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3014</td>
      <td>Alicante/Alacant</td>
      <td>38º 20' 46"</td>
      <td>-00º 28' 38"</td>
    </tr>
    <tr>
      <th>3</th>
      <td>301410</td>
      <td>Saladar</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3014</td>
      <td>Alicante/Alacant</td>
      <td>38º 17' 02"</td>
      <td>-00º 31' 08"</td>
    </tr>
    <tr>
      <th>4</th>
      <td>301808</td>
      <td>La Roda</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3018</td>
      <td>Altea</td>
      <td>38º 36' 29"</td>
      <td>-00º 02' 16"</td>
    </tr>
  </tbody>
</table>
</div>




```python
ids = df_codigos["ID_PLAYA"].astype(str).str.zfill(7).head(10)
print("IDs:", ids.tolist())
```

    IDs: ['0301101', '0301401', '0301408', '0301410', '0301808', '0301809', '0303102', '0303104', '0304105', '0304704']



```python
s3 = boto3.client("s3")
ahora = datetime.utcnow()

ids = df_codigos["ID_PLAYA"].astype(str).str.zfill(7).head(10)

for id_playa in ids:
    print("Playa:", id_playa)

    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/playa/{id_playa}"

    r = requests.get(url, headers={"api_key": API_KEY})
    data = r.json()

    print(data)

    if "datos" not in data:
        print("No existe 'datos' para esta playa")
        continue

    url_datos = data["datos"]
    r2 = requests.get(url_datos, headers={"api_key": API_KEY})

    try:
        datos = r2.json()
    except:
        datos = {"raw": r2.text}

    key = (
        f"meteorologia/prediccion_playas/"
        f"year={ahora:%Y}/month={ahora:%m}/day={ahora:%d}/"
        f"playa_{id_playa}.json"
    )

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(datos).encode("utf-8")
    )

    print("Subido:", key)
```

    Playa: 0301101
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/7d93919c', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0301101.json
    Playa: 0301401
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/c32641f7', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0301401.json
    Playa: 0301408
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/27ac023c', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0301408.json
    Playa: 0301410
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/65ada4a2', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0301410.json
    Playa: 0301808
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/8003bb56', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0301808.json
    Playa: 0301809
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/6319041a', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0301809.json
    Playa: 0303102
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/3d209de7', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0303102.json
    Playa: 0303104
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/e21fc857', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0303104.json
    Playa: 0304105
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/3731182c', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0304105.json
    Playa: 0304704
    {'descripcion': 'exito', 'estado': 200, 'datos': 'https://opendata.aemet.es/opendata/sh/b91f7f92', 'metadatos': 'https://opendata.aemet.es/opendata/sh/8ca2e7e3'}
    Subido: meteorologia/prediccion_playas/year=2026/month=04/day=10/playa_0304704.json


![imagen.png](19caed71-a5b0-4ee8-b912-995fdae6d186.png)


```python

```
