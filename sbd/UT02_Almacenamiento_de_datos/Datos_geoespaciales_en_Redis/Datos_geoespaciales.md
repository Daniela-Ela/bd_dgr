```python
import redis
import datetime

r = redis.Redis(host='redis-server', port=6379, db=0, decode_responses=True)
```

PR0204: Estructuras de datos avanzadas: datos geoespaciales

Tarea 1: Carga de datos

El objetivo de esta tareaa será poblar la base de datos Redis con los puntos de interés.

Los requisitos son:

Crear un script load_locations.py.
Utiliza la estructura de datos que está en el fichero locations.py con POIs de Madrid
El script debe conectarse a Redis y, en un bucle: - Añadir la ubicación: usa r.geoadd("poi:locations", (longitud, latitud, id)) - Guardar el nombre: usa r.hset("poi:info", id, "Nombre del POI")
Imprimir un mensaje de “Datos cargados” al finalizar.


```python
from locations import POIS
```


```python
POIS
```




    [{'id': 'poi_001',
      'name': 'Puerta del Sol',
      'lon': -3.70379,
      'lat': 40.416775},
     {'id': 'poi_002',
      'name': 'Museo del Prado',
      'lon': -3.69214,
      'lat': 40.41378},
     {'id': 'poi_003',
      'name': 'Parque del Retiro',
      'lon': -3.68444,
      'lat': 40.41536},
     {'id': 'poi_004', 'name': 'Palacio Real', 'lon': -3.71431, 'lat': 40.41791},
     {'id': 'poi_005', 'name': 'Plaza Mayor', 'lon': -3.70737, 'lat': 40.41538},
     {'id': 'poi_006',
      'name': 'Museo Reina Sofía',
      'lon': -3.69434,
      'lat': 40.40801},
     {'id': 'poi_007',
      'name': 'Museo Thyssen-Bornemisza',
      'lon': -3.695,
      'lat': 40.4161},
     {'id': 'poi_008',
      'name': 'Estadio Santiago Bernabéu',
      'lon': -3.69238,
      'lat': 40.45305},
     {'id': 'poi_009',
      'name': 'Gran Vía (Plaza Callao)',
      'lon': -3.708,
      'lat': 40.4202},
     {'id': 'poi_010', 'name': 'Templo de Debod', 'lon': -3.718, 'lat': 40.4243},
     {'id': 'poi_011',
      'name': 'Mercado de San Miguel',
      'lon': -3.7093,
      'lat': 40.415},
     {'id': 'poi_012',
      'name': 'Catedral de la Almudena',
      'lon': -3.7142,
      'lat': 40.416},
     {'id': 'poi_013',
      'name': 'Estación de Atocha',
      'lon': -3.6905,
      'lat': 40.4069},
     {'id': 'poi_014', 'name': 'Plaza de Cibeles', 'lon': -3.693, 'lat': 40.4192},
     {'id': 'poi_015', 'name': 'Puerta de Alcalá', 'lon': -3.6887, 'lat': 40.4205},
     {'id': 'poi_016', 'name': 'Plaza de España', 'lon': -3.712, 'lat': 40.4239},
     {'id': 'poi_017',
      'name': 'CaixaForum Madrid',
      'lon': -3.6934,
      'lat': 40.4093},
     {'id': 'poi_018',
      'name': 'Plaza de Cascorro (El Rastro)',
      'lon': -3.7067,
      'lat': 40.4111},
     {'id': 'poi_019', 'name': 'Matadero Madrid', 'lon': -3.7032, 'lat': 40.3916},
     {'id': 'poi_020',
      'name': 'Estadio Cívitas Metropolitano',
      'lon': -3.5991,
      'lat': 40.4363}]




```python
for poi in POIS:
    r.geoadd("poi:locations", (poi["lon"], poi["lat"], poi["id"]))
    r.hset("poi:info", poi["id"], poi["name"])

print("Datos cargados correctamente.")
```

    Datos cargados correctamente.


Tarea 2: Búsqueda por radio

El objetivo de esta función es encontrar todos los POIs dentro de un radio específico desde la ubicación del usuario.

Los pasos a realizar son:

Crea un script find_by_radius.py(lat, lon, distance=2000).
Define una ubicación de “Usuario” (p.ej., lat=40.41677, lon=-3.70379, que es la Puerta del Sol).
Usa el comando GEOSERACH para encontrar todos los POIs en un radio.
Para cada POI encontrado (que será un id) consulta el HASH poi:info para obtener su nombre.
Imprime un informe: Encontrados X POIs en 2 km:
-> Museo del Prado (id_001)
-> Palacio Real (id_003)


```python
def find_by_radius(lat, lon, distance=2000):
    poi_ids = r.geosearch(
        "poi:locations",
        longitude=lon,
        latitude=lat,
        radius=distance,
        unit="m"
    )

    print(f"Encontrados {len(poi_ids)} POIs en {distance/1000} km:\n")

    for poi_id in poi_ids:
        name = r.hget("poi:info", poi_id)
        print(f" -> {name} ({poi_id})")

```


```python
find_by_radius(
    lat=40.41677,
    lon=-3.70379,
    distance=2000   
)
```

    Encontrados 17 POIs en 2.0 km:
    
     -> Catedral de la Almudena (poi_012)
     -> Palacio Real (poi_004)
     -> Templo de Debod (poi_010)
     -> Plaza de Cascorro (El Rastro) (poi_018)
     -> Mercado de San Miguel (poi_011)
     -> Plaza Mayor (poi_005)
     -> Puerta del Sol (poi_001)
     -> Museo Reina Sofía (poi_006)
     -> CaixaForum Madrid (poi_017)
     -> Museo del Prado (poi_002)
     -> Museo Thyssen-Bornemisza (poi_007)
     -> Gran Vía (Plaza Callao) (poi_009)
     -> Plaza de España (poi_016)
     -> Plaza de Cibeles (poi_014)
     -> Parque del Retiro (poi_003)
     -> Puerta de Alcalá (poi_015)
     -> Estación de Atocha (poi_013)



```python

```
