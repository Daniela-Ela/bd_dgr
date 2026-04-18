# **PR0303: Obtención de datos de una API REST**

## **Práctica: Ingesta de Datos con Star Wars API (SWAPI)**

El objetivo de esta práctica será desarrollar un script en Python que extraiga información de swapi.dev y la transforme en DataFrames de Pandas listos para el análisis.


```python
!pip install requests
import requests
import pandas as pd
```

    Requirement already satisfied: requests in /opt/conda/lib/python3.11/site-packages (2.31.0)
    Requirement already satisfied: charset-normalizer<4,>=2 in /opt/conda/lib/python3.11/site-packages (from requests) (3.3.0)
    Requirement already satisfied: idna<4,>=2.5 in /opt/conda/lib/python3.11/site-packages (from requests) (3.4)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/conda/lib/python3.11/site-packages (from requests) (2.0.7)
    Requirement already satisfied: certifi>=2017.4.17 in /opt/conda/lib/python3.11/site-packages (from requests) (2023.7.22)


### **1.- Conexión básica y primer dataFrame**

En esta fase, debes conectar con el endpoint de **Vehículos** y extraer la primera página de resultados (10 elementos).

Los pasos a realizar son:
1. Realizar una petición ``GET`` al endpoint ``https://swapi.dev/api/vehicles/``.
2. Extrae la clave ``results`` del JSON de respuesta.
3. Convierte esa lista de diccionarios en un dataframe de Pandas.
4. Muestra las primeras 5 filas y el nombre de las columnas obtenidas.


```python
url = 'https://swapi.dev/api/vehicles/'

response = requests.get(url)

if response.status_code == 200:
    print("¡Éxito! Conexión establecida.")
    datos = response.json()
    print(datos)
else:
    print(f"Error: {response.status_code}")
    
```

    ¡Éxito! Conexión establecida.
    {'count': 39, 'next': 'https://swapi.dev/api/vehicles/?page=2', 'previous': None, 'results': [{'name': 'Sand Crawler', 'model': 'Digger Crawler', 'manufacturer': 'Corellia Mining Corporation', 'cost_in_credits': '150000', 'length': '36.8 ', 'max_atmosphering_speed': '30', 'crew': '46', 'passengers': '30', 'cargo_capacity': '50000', 'consumables': '2 months', 'vehicle_class': 'wheeled', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/', 'https://swapi.dev/api/films/5/'], 'created': '2014-12-10T15:36:25.724000Z', 'edited': '2014-12-20T21:30:21.661000Z', 'url': 'https://swapi.dev/api/vehicles/4/'}, {'name': 'T-16 skyhopper', 'model': 'T-16 skyhopper', 'manufacturer': 'Incom Corporation', 'cost_in_credits': '14500', 'length': '10.4 ', 'max_atmosphering_speed': '1200', 'crew': '1', 'passengers': '1', 'cargo_capacity': '50', 'consumables': '0', 'vehicle_class': 'repulsorcraft', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/'], 'created': '2014-12-10T16:01:52.434000Z', 'edited': '2014-12-20T21:30:21.665000Z', 'url': 'https://swapi.dev/api/vehicles/6/'}, {'name': 'X-34 landspeeder', 'model': 'X-34 landspeeder', 'manufacturer': 'SoroSuub Corporation', 'cost_in_credits': '10550', 'length': '3.4 ', 'max_atmosphering_speed': '250', 'crew': '1', 'passengers': '1', 'cargo_capacity': '5', 'consumables': 'unknown', 'vehicle_class': 'repulsorcraft', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/'], 'created': '2014-12-10T16:13:52.586000Z', 'edited': '2014-12-20T21:30:21.668000Z', 'url': 'https://swapi.dev/api/vehicles/7/'}, {'name': 'TIE/LN starfighter', 'model': 'Twin Ion Engine/Ln Starfighter', 'manufacturer': 'Sienar Fleet Systems', 'cost_in_credits': 'unknown', 'length': '6.4', 'max_atmosphering_speed': '1200', 'crew': '1', 'passengers': '0', 'cargo_capacity': '65', 'consumables': '2 days', 'vehicle_class': 'starfighter', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/', 'https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-10T16:33:52.860000Z', 'edited': '2014-12-20T21:30:21.670000Z', 'url': 'https://swapi.dev/api/vehicles/8/'}, {'name': 'Snowspeeder', 'model': 't-47 airspeeder', 'manufacturer': 'Incom corporation', 'cost_in_credits': 'unknown', 'length': '4.5', 'max_atmosphering_speed': '650', 'crew': '2', 'passengers': '0', 'cargo_capacity': '10', 'consumables': 'none', 'vehicle_class': 'airspeeder', 'pilots': ['https://swapi.dev/api/people/1/', 'https://swapi.dev/api/people/18/'], 'films': ['https://swapi.dev/api/films/2/'], 'created': '2014-12-15T12:22:12Z', 'edited': '2014-12-20T21:30:21.672000Z', 'url': 'https://swapi.dev/api/vehicles/14/'}, {'name': 'TIE bomber', 'model': 'TIE/sa bomber', 'manufacturer': 'Sienar Fleet Systems', 'cost_in_credits': 'unknown', 'length': '7.8', 'max_atmosphering_speed': '850', 'crew': '1', 'passengers': '0', 'cargo_capacity': 'none', 'consumables': '2 days', 'vehicle_class': 'space/planetary bomber', 'pilots': [], 'films': ['https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-15T12:33:15.838000Z', 'edited': '2014-12-20T21:30:21.675000Z', 'url': 'https://swapi.dev/api/vehicles/16/'}, {'name': 'AT-AT', 'model': 'All Terrain Armored Transport', 'manufacturer': 'Kuat Drive Yards, Imperial Department of Military Research', 'cost_in_credits': 'unknown', 'length': '20', 'max_atmosphering_speed': '60', 'crew': '5', 'passengers': '40', 'cargo_capacity': '1000', 'consumables': 'unknown', 'vehicle_class': 'assault walker', 'pilots': [], 'films': ['https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-15T12:38:25.937000Z', 'edited': '2014-12-20T21:30:21.677000Z', 'url': 'https://swapi.dev/api/vehicles/18/'}, {'name': 'AT-ST', 'model': 'All Terrain Scout Transport', 'manufacturer': 'Kuat Drive Yards, Imperial Department of Military Research', 'cost_in_credits': 'unknown', 'length': '2', 'max_atmosphering_speed': '90', 'crew': '2', 'passengers': '0', 'cargo_capacity': '200', 'consumables': 'none', 'vehicle_class': 'walker', 'pilots': ['https://swapi.dev/api/people/13/'], 'films': ['https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-15T12:46:42.384000Z', 'edited': '2014-12-20T21:30:21.679000Z', 'url': 'https://swapi.dev/api/vehicles/19/'}, {'name': 'Storm IV Twin-Pod cloud car', 'model': 'Storm IV Twin-Pod', 'manufacturer': 'Bespin Motors', 'cost_in_credits': '75000', 'length': '7', 'max_atmosphering_speed': '1500', 'crew': '2', 'passengers': '0', 'cargo_capacity': '10', 'consumables': '1 day', 'vehicle_class': 'repulsorcraft', 'pilots': [], 'films': ['https://swapi.dev/api/films/2/'], 'created': '2014-12-15T12:58:50.530000Z', 'edited': '2014-12-20T21:30:21.681000Z', 'url': 'https://swapi.dev/api/vehicles/20/'}, {'name': 'Sail barge', 'model': 'Modified Luxury Sail Barge', 'manufacturer': 'Ubrikkian Industries Custom Vehicle Division', 'cost_in_credits': '285000', 'length': '30', 'max_atmosphering_speed': '100', 'crew': '26', 'passengers': '500', 'cargo_capacity': '2000000', 'consumables': 'Live food tanks', 'vehicle_class': 'sail barge', 'pilots': [], 'films': ['https://swapi.dev/api/films/3/'], 'created': '2014-12-18T10:44:14.217000Z', 'edited': '2014-12-20T21:30:21.684000Z', 'url': 'https://swapi.dev/api/vehicles/24/'}]}



```python
pd.json_normalize(datos)
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
      <th>count</th>
      <th>next</th>
      <th>previous</th>
      <th>results</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>39</td>
      <td>https://swapi.dev/api/vehicles/?page=2</td>
      <td>None</td>
      <td>[{'name': 'Sand Crawler', 'model': 'Digger Cra...</td>
    </tr>
  </tbody>
</table>
</div>




```python
data = response.json()
results = data["results"]
print(results)
```

    [{'name': 'Sand Crawler', 'model': 'Digger Crawler', 'manufacturer': 'Corellia Mining Corporation', 'cost_in_credits': '150000', 'length': '36.8 ', 'max_atmosphering_speed': '30', 'crew': '46', 'passengers': '30', 'cargo_capacity': '50000', 'consumables': '2 months', 'vehicle_class': 'wheeled', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/', 'https://swapi.dev/api/films/5/'], 'created': '2014-12-10T15:36:25.724000Z', 'edited': '2014-12-20T21:30:21.661000Z', 'url': 'https://swapi.dev/api/vehicles/4/'}, {'name': 'T-16 skyhopper', 'model': 'T-16 skyhopper', 'manufacturer': 'Incom Corporation', 'cost_in_credits': '14500', 'length': '10.4 ', 'max_atmosphering_speed': '1200', 'crew': '1', 'passengers': '1', 'cargo_capacity': '50', 'consumables': '0', 'vehicle_class': 'repulsorcraft', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/'], 'created': '2014-12-10T16:01:52.434000Z', 'edited': '2014-12-20T21:30:21.665000Z', 'url': 'https://swapi.dev/api/vehicles/6/'}, {'name': 'X-34 landspeeder', 'model': 'X-34 landspeeder', 'manufacturer': 'SoroSuub Corporation', 'cost_in_credits': '10550', 'length': '3.4 ', 'max_atmosphering_speed': '250', 'crew': '1', 'passengers': '1', 'cargo_capacity': '5', 'consumables': 'unknown', 'vehicle_class': 'repulsorcraft', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/'], 'created': '2014-12-10T16:13:52.586000Z', 'edited': '2014-12-20T21:30:21.668000Z', 'url': 'https://swapi.dev/api/vehicles/7/'}, {'name': 'TIE/LN starfighter', 'model': 'Twin Ion Engine/Ln Starfighter', 'manufacturer': 'Sienar Fleet Systems', 'cost_in_credits': 'unknown', 'length': '6.4', 'max_atmosphering_speed': '1200', 'crew': '1', 'passengers': '0', 'cargo_capacity': '65', 'consumables': '2 days', 'vehicle_class': 'starfighter', 'pilots': [], 'films': ['https://swapi.dev/api/films/1/', 'https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-10T16:33:52.860000Z', 'edited': '2014-12-20T21:30:21.670000Z', 'url': 'https://swapi.dev/api/vehicles/8/'}, {'name': 'Snowspeeder', 'model': 't-47 airspeeder', 'manufacturer': 'Incom corporation', 'cost_in_credits': 'unknown', 'length': '4.5', 'max_atmosphering_speed': '650', 'crew': '2', 'passengers': '0', 'cargo_capacity': '10', 'consumables': 'none', 'vehicle_class': 'airspeeder', 'pilots': ['https://swapi.dev/api/people/1/', 'https://swapi.dev/api/people/18/'], 'films': ['https://swapi.dev/api/films/2/'], 'created': '2014-12-15T12:22:12Z', 'edited': '2014-12-20T21:30:21.672000Z', 'url': 'https://swapi.dev/api/vehicles/14/'}, {'name': 'TIE bomber', 'model': 'TIE/sa bomber', 'manufacturer': 'Sienar Fleet Systems', 'cost_in_credits': 'unknown', 'length': '7.8', 'max_atmosphering_speed': '850', 'crew': '1', 'passengers': '0', 'cargo_capacity': 'none', 'consumables': '2 days', 'vehicle_class': 'space/planetary bomber', 'pilots': [], 'films': ['https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-15T12:33:15.838000Z', 'edited': '2014-12-20T21:30:21.675000Z', 'url': 'https://swapi.dev/api/vehicles/16/'}, {'name': 'AT-AT', 'model': 'All Terrain Armored Transport', 'manufacturer': 'Kuat Drive Yards, Imperial Department of Military Research', 'cost_in_credits': 'unknown', 'length': '20', 'max_atmosphering_speed': '60', 'crew': '5', 'passengers': '40', 'cargo_capacity': '1000', 'consumables': 'unknown', 'vehicle_class': 'assault walker', 'pilots': [], 'films': ['https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-15T12:38:25.937000Z', 'edited': '2014-12-20T21:30:21.677000Z', 'url': 'https://swapi.dev/api/vehicles/18/'}, {'name': 'AT-ST', 'model': 'All Terrain Scout Transport', 'manufacturer': 'Kuat Drive Yards, Imperial Department of Military Research', 'cost_in_credits': 'unknown', 'length': '2', 'max_atmosphering_speed': '90', 'crew': '2', 'passengers': '0', 'cargo_capacity': '200', 'consumables': 'none', 'vehicle_class': 'walker', 'pilots': ['https://swapi.dev/api/people/13/'], 'films': ['https://swapi.dev/api/films/2/', 'https://swapi.dev/api/films/3/'], 'created': '2014-12-15T12:46:42.384000Z', 'edited': '2014-12-20T21:30:21.679000Z', 'url': 'https://swapi.dev/api/vehicles/19/'}, {'name': 'Storm IV Twin-Pod cloud car', 'model': 'Storm IV Twin-Pod', 'manufacturer': 'Bespin Motors', 'cost_in_credits': '75000', 'length': '7', 'max_atmosphering_speed': '1500', 'crew': '2', 'passengers': '0', 'cargo_capacity': '10', 'consumables': '1 day', 'vehicle_class': 'repulsorcraft', 'pilots': [], 'films': ['https://swapi.dev/api/films/2/'], 'created': '2014-12-15T12:58:50.530000Z', 'edited': '2014-12-20T21:30:21.681000Z', 'url': 'https://swapi.dev/api/vehicles/20/'}, {'name': 'Sail barge', 'model': 'Modified Luxury Sail Barge', 'manufacturer': 'Ubrikkian Industries Custom Vehicle Division', 'cost_in_credits': '285000', 'length': '30', 'max_atmosphering_speed': '100', 'crew': '26', 'passengers': '500', 'cargo_capacity': '2000000', 'consumables': 'Live food tanks', 'vehicle_class': 'sail barge', 'pilots': [], 'films': ['https://swapi.dev/api/films/3/'], 'created': '2014-12-18T10:44:14.217000Z', 'edited': '2014-12-20T21:30:21.684000Z', 'url': 'https://swapi.dev/api/vehicles/24/'}]



```python
df_vehicles = pd.DataFrame(results)
print(df_vehicles.head())
```

                     name                           model  \
    0        Sand Crawler                  Digger Crawler   
    1      T-16 skyhopper                  T-16 skyhopper   
    2    X-34 landspeeder                X-34 landspeeder   
    3  TIE/LN starfighter  Twin Ion Engine/Ln Starfighter   
    4         Snowspeeder                 t-47 airspeeder   
    
                      manufacturer cost_in_credits length max_atmosphering_speed  \
    0  Corellia Mining Corporation          150000  36.8                      30   
    1            Incom Corporation           14500  10.4                    1200   
    2         SoroSuub Corporation           10550   3.4                     250   
    3         Sienar Fleet Systems         unknown    6.4                   1200   
    4            Incom corporation         unknown    4.5                    650   
    
      crew passengers cargo_capacity consumables  vehicle_class  \
    0   46         30          50000    2 months        wheeled   
    1    1          1             50           0  repulsorcraft   
    2    1          1              5     unknown  repulsorcraft   
    3    1          0             65      2 days    starfighter   
    4    2          0             10        none     airspeeder   
    
                                                  pilots  \
    0                                                 []   
    1                                                 []   
    2                                                 []   
    3                                                 []   
    4  [https://swapi.dev/api/people/1/, https://swap...   
    
                                                   films  \
    0  [https://swapi.dev/api/films/1/, https://swapi...   
    1                   [https://swapi.dev/api/films/1/]   
    2                   [https://swapi.dev/api/films/1/]   
    3  [https://swapi.dev/api/films/1/, https://swapi...   
    4                   [https://swapi.dev/api/films/2/]   
    
                           created                       edited  \
    0  2014-12-10T15:36:25.724000Z  2014-12-20T21:30:21.661000Z   
    1  2014-12-10T16:01:52.434000Z  2014-12-20T21:30:21.665000Z   
    2  2014-12-10T16:13:52.586000Z  2014-12-20T21:30:21.668000Z   
    3  2014-12-10T16:33:52.860000Z  2014-12-20T21:30:21.670000Z   
    4         2014-12-15T12:22:12Z  2014-12-20T21:30:21.672000Z   
    
                                      url  
    0   https://swapi.dev/api/vehicles/4/  
    1   https://swapi.dev/api/vehicles/6/  
    2   https://swapi.dev/api/vehicles/7/  
    3   https://swapi.dev/api/vehicles/8/  
    4  https://swapi.dev/api/vehicles/14/  



```python
print("\nNúmero de columnas:", df_vehicles.shape[1])
print("Columnas:", df_vehicles.columns.tolist())
```

    
    Número de columnas: 16
    Columnas: ['name', 'model', 'manufacturer', 'cost_in_credits', 'length', 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'vehicle_class', 'pilots', 'films', 'created', 'edited', 'url']


### **2.- Gestión de paginación**

La API de Star Wars devuelve los resultados de 10 en 10. Pero necesitamos el dataset completo de **personajes (people)**.

En este apartado debes:

1. Implementar un bucle (``while``) que verifique la existencia de la clave ``next`` en el JSON.
2. Iterar por todas las páginas (aprox. 82 personajes) recolectando los datos en una lista global.
3. Crear un DataFrame único con todos los registros.
4. Verifica que el DataFrame resultante tenga el mismo número de filas que el valor indicado en la clave ``count`` de la API.


```python
import requests
import pandas as pd

url = "https://swapi.dev/api/people/"
personajes = []
total = None

while url:
    respuesta = requests.get(url)
    datos = respuesta.json()

    if total is None:
        total = datos["count"]

    personajes.extend(datos["results"])
    url = datos["next"]

df_people = pd.DataFrame(personajes)

df_people["name"].value_counts()
```




    name
    Luke Skywalker       1
    Poggle the Lesser    1
    Cordé                1
    Gregar Typho         1
    Mas Amedda           1
                        ..
    Mon Mothma           1
    Ackbar               1
    Lobot                1
    Lando Calrissian     1
    Tion Medon           1
    Name: count, Length: 82, dtype: int64



### **3.- Cruce de datos**

En este punto vamos a combinar datos de diferentes endpoints, en concreto, enriqueceremos los datos de personajes obtenidos en el punto anterior con información de su planeta de origen.

Tienes que hacer lo siguiente:
1. La columna ``homeworld`` de cada personaje es una URL (ej: ``https://swapi.dev/api/planets/1/``).
2. Crea una función que reciba esa URL y devuelva una tupla con el **nombre, terreno y población del planeta** (haciendo una nueva petición a la API).
3. Aplica esta función a los primeros 20 personajes del DataFrame (para no saturar la API) y añade al dataframe de personajes los datos correspondientes a su planeta.


```python
df_mini = df_people.head(20).copy()

def obtener_planeta(url):
    
    if not url:
        return pd.Series(["Desconocido", "Desconocido", "Desconocido"])
    
    try:
        r = requests.get(url)
        data = r.json()
        
        return pd.Series([data.get("name"), data.get("terrain"), data.get("population")])
    
    except:
        return pd.Series(["Error", "Error", "Error"])

df_mini[["planet_name", "planet_terrain", "planet_population"]] = \
    df_mini["homeworld"].apply(obtener_planeta)


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
      <th>name</th>
      <th>height</th>
      <th>mass</th>
      <th>hair_color</th>
      <th>skin_color</th>
      <th>eye_color</th>
      <th>birth_year</th>
      <th>gender</th>
      <th>homeworld</th>
      <th>films</th>
      <th>species</th>
      <th>vehicles</th>
      <th>starships</th>
      <th>created</th>
      <th>edited</th>
      <th>url</th>
      <th>planet_name</th>
      <th>planet_terrain</th>
      <th>planet_population</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C-3PO</td>
      <td>167</td>
      <td>75</td>
      <td>n/a</td>
      <td>gold</td>
      <td>yellow</td>
      <td>112BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:10:51.357000Z</td>
      <td>2014-12-20T21:17:50.309000Z</td>
      <td>https://swapi.dev/api/people/2/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R2-D2</td>
      <td>96</td>
      <td>32</td>
      <td>n/a</td>
      <td>white, blue</td>
      <td>red</td>
      <td>33BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/8/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:11:50.376000Z</td>
      <td>2014-12-20T21:17:50.311000Z</td>
      <td>https://swapi.dev/api/people/3/</td>
      <td>Naboo</td>
      <td>grassy hills, swamps, forests, mountains</td>
      <td>4500000000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Darth Vader</td>
      <td>202</td>
      <td>136</td>
      <td>none</td>
      <td>white</td>
      <td>yellow</td>
      <td>41.9BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/starships/13/]</td>
      <td>2014-12-10T15:18:20.704000Z</td>
      <td>2014-12-20T21:17:50.313000Z</td>
      <td>https://swapi.dev/api/people/4/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Leia Organa</td>
      <td>150</td>
      <td>49</td>
      <td>brown</td>
      <td>light</td>
      <td>brown</td>
      <td>19BBY</td>
      <td>female</td>
      <td>https://swapi.dev/api/planets/2/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/30/]</td>
      <td>[]</td>
      <td>2014-12-10T15:20:09.791000Z</td>
      <td>2014-12-20T21:17:50.315000Z</td>
      <td>https://swapi.dev/api/people/5/</td>
      <td>Alderaan</td>
      <td>grasslands, mountains</td>
      <td>2000000000</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
