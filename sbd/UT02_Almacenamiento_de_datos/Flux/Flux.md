# **PR0207: Consultas con Flux**

## **PARTE I: Consultas de filtrado y estructura**

El objetivo es familiarizarse con el inicio de la pipeline y el uso de Tags para filtrar.

### **Tarea 1.1: Precio de cierre de Bitcoin**

Escribe una consulta en Flux que:

1. Use el bucket **``crypto_raw``**.
2. Consulte los datos de de diciembre de 2020 (``range``).
3. Filtre solo el activo **``BTC``** (usando el Tag ``symbol``).
4. Filtre solo el campo **``close``** (usando el Field ``_field``).


```python
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point

INFLUX_URL = "http://influxdb-influxdb2-1:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="

print("--- Iniciando conexión a InfluxDB ---")

client = None

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org="docs"
        )
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    health = client.health()
    
    if health.status == "pass":
        print("[INFO] ¡Conexión Exitosa!")
        print(f"[INFO] Versión del servidor: {health.version}")
        ##Aqui va la logica
        ejer = """
from(bucket: "crypto_raw")
  |> range(start: 2020-12-01T00:00:00Z, stop: 2020-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "daily_quotes")
  |> filter(fn: (r) => r["_field"] == "close")
  |> filter(fn: (r) => r["name"] == "Bitcoin")

        """
        query_api = client.query_api()

        print("[INFO] Ejecutando consulta")
        tables = query_api.query(query=ejer, org="docs")
        
        for table in tables:
            for record in table.records:
                print(
                    f"Time: {record.get_time()} | "
                    f"Close: {record.get_value()}"
                )

    
    else:
        print(f"[Error] Conexion fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")
except (InfluxDBError,NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f" Detalle: {e}")
finally:
    if client:
        client.close()
        print("--- Conexión Cerrada ---")
```

    --- Iniciando conexión a InfluxDB ---
    Verificando estado de salud de InfluxDB en http://influxdb-influxdb2-1:8086
    [INFO] ¡Conexión Exitosa!
    [INFO] Versión del servidor: v2.7.12
    [INFO] Ejecutando consulta
    Time: 2020-12-01 23:59:59+00:00 | Close: 18802.99829969
    Time: 2020-12-02 23:59:59+00:00 | Close: 19201.09115697
    Time: 2020-12-03 23:59:59+00:00 | Close: 19445.39847988
    Time: 2020-12-04 23:59:59+00:00 | Close: 18699.76561337
    Time: 2020-12-05 23:59:59+00:00 | Close: 19154.231131
    Time: 2020-12-06 23:59:59+00:00 | Close: 19345.12095871
    Time: 2020-12-07 23:59:59+00:00 | Close: 19191.63128698
    Time: 2020-12-08 23:59:59+00:00 | Close: 18321.14491611
    Time: 2020-12-09 23:59:59+00:00 | Close: 18553.91537685
    Time: 2020-12-10 23:59:59+00:00 | Close: 18264.99210672
    Time: 2020-12-11 23:59:59+00:00 | Close: 18058.90334725
    Time: 2020-12-12 23:59:59+00:00 | Close: 18803.65687045
    Time: 2020-12-13 23:59:59+00:00 | Close: 19142.3825335
    Time: 2020-12-14 23:59:59+00:00 | Close: 19246.64434137
    Time: 2020-12-15 23:59:59+00:00 | Close: 19417.07603342
    Time: 2020-12-16 23:59:59+00:00 | Close: 21310.59813054
    Time: 2020-12-17 23:59:59+00:00 | Close: 22805.16149213
    Time: 2020-12-18 23:59:59+00:00 | Close: 23137.96056165
    Time: 2020-12-19 23:59:59+00:00 | Close: 23869.83196434
    Time: 2020-12-20 23:59:59+00:00 | Close: 23477.29519711
    Time: 2020-12-21 23:59:59+00:00 | Close: 22803.0814087
    Time: 2020-12-22 23:59:59+00:00 | Close: 23783.02850288
    Time: 2020-12-23 23:59:59+00:00 | Close: 23241.34486501
    Time: 2020-12-24 23:59:59+00:00 | Close: 23735.94972763
    Time: 2020-12-25 23:59:59+00:00 | Close: 24664.79027412
    Time: 2020-12-26 23:59:59+00:00 | Close: 26437.0375091
    Time: 2020-12-27 23:59:59+00:00 | Close: 26272.29456706
    Time: 2020-12-28 23:59:59+00:00 | Close: 27084.80788628
    Time: 2020-12-29 23:59:59+00:00 | Close: 27362.4365573
    Time: 2020-12-30 23:59:59+00:00 | Close: 28840.95341968
    --- Conexión Cerrada ---


![imagen.png](b920284b-a23c-4668-9109-42c82ef888bc.png)

### **Tarea 1.2: Volumen Total del Ethereum (ETHUSDT)**

Escribe una consulta que:

1. Filtre los datos de **``ETH``** de **enero a junio de 2021**.
2. Filtre el campo **``volume``**.
3. Use la función de agregación **``sum()``** para calcular el volumen total de transacciones en ese periodo.


```python
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point

INFLUX_URL = "http://influxdb-influxdb2-1:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="

print("--- Iniciando conexión a InfluxDB ---")

client = None

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org="docs"
        )
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    health = client.health()
    
    if health.status == "pass":
        print("[INFO] ¡Conexión Exitosa!")
        print(f"[INFO] Versión del servidor: {health.version}")
        ##Aqui va la logica
        ejer = """
    from(bucket: "crypto_raw")
  |> range(start: 2021-01-01T00:00:00Z, stop: 2021-06-30T23:59:59Z)
  |> filter(fn: (r) => r._measurement == "daily_quote")
  |> filter(fn: (r) => r._field == "volume")
  |> filter(fn: (r) => r.symbol == "ETH")
  |> sum()
        """
        query_api = client.query_api()

        print("[INFO] Ejecutando consulta")
        tables = query_api.query(query=ejer, org="docs")
        
        for table in tables:
            for record in table.records:
                print(
                    f"Time: {record.get_time()} | "
                    f"Close: {record.get_value()}"
                )

    
    else:
        print(f"[Error] Conexion fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")
except (InfluxDBError,NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f" Detalle: {e}")
finally:
    if client:
        client.close()
        print("--- Conexión Cerrada ---")
```

    --- Iniciando conexión a InfluxDB ---
    Verificando estado de salud de InfluxDB en http://influxdb-influxdb2-1:8086
    [INFO] ¡Conexión Exitosa!
    [INFO] Versión del servidor: v2.7.12
    [INFO] Ejecutando consulta
    --- Conexión Cerrada ---


## **PARTE II: Agregación temporal**

Aquí se introduce el concepto clave de las series de tiempo: la agregación por ventanas de tiempo.

### **Tarea 2.1: Precio promedio mensual**

Escribe una consulta que:

1. Filtre los precios de cierre (``close``) de **``BTC``** de todo el histórico disponible.
2. Use la función **``aggregateWindow()``** para calcular el **precio promedio** (**``fn: mean``**) por mes (**``every: 1mo``**).
3. Resultado esperado: Una fila por mes, mostrando la media del precio de cierre de BTC en ese mes.


```python
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point

INFLUX_URL = "http://influxdb-influxdb2-1:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="

print("--- Iniciando conexión a InfluxDB ---")

client = None

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org="docs"
        )
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    health = client.health()
    
    if health.status == "pass":
        print("[INFO] ¡Conexión Exitosa!")
        print(f"[INFO] Versión del servidor: {health.version}")
        ##Aqui va la logica
        tarea = """
from(bucket: "crypto_raw")
  |> range(start: 2010-01-01T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "daily_quotes")
  |> filter(fn: (r) => r._field == "close")
  |> filter(fn: (r) => r.name == "Bitcoin")
  |> aggregateWindow(every: 1mo, fn: mean, createEmpty: false)
        """
        query_api = client.query_api()

        print("[INFO] Ejecutando consulta")
        tables = query_api.query(query=tarea, org="docs")
        
        for table in tables:
            for record in table.records:
                print(
                    f"Time: {record.get_time()} | "
                    f"Close: {record.get_value()}"
                )
    
    else:
        print(f"[Error] Conexion fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")
except (InfluxDBError,NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f" Detalle: {e}")
finally:
    if client:
        client.close()
        print("--- Conexión Cerrada ---")
```

    --- Iniciando conexión a InfluxDB ---
    Verificando estado de salud de InfluxDB en http://influxdb-influxdb2-1:8086
    [INFO] ¡Conexión Exitosa!
    [INFO] Versión del servidor: v2.7.12
    [INFO] Ejecutando consulta
    Time: 2013-05-01 00:00:00+00:00 | Close: 141.7699966430664
    Time: 2013-06-01 00:00:00+00:00 | Close: 119.99274124637726
    Time: 2013-07-01 00:00:00+00:00 | Close: 107.76140670776367
    Time: 2013-08-01 00:00:00+00:00 | Close: 90.512206539031
    Time: 2013-09-01 00:00:00+00:00 | Close: 113.90548435334236
    Time: 2013-10-01 00:00:00+00:00 | Close: 130.0616668701172
    Time: 2013-11-01 00:00:00+00:00 | Close: 158.3119359170237
    Time: 2013-12-01 00:00:00+00:00 | Close: 550.420664469401
    Time: 2014-01-01 00:00:00+00:00 | Close: 800.7809664818549
    Time: 2014-02-01 00:00:00+00:00 | Close: 844.1683900894657
    Time: 2014-03-01 00:00:00+00:00 | Close: 661.6182163783482
    Time: 2014-04-01 00:00:00+00:00 | Close: 592.2003843245968
    Time: 2014-05-01 00:00:00+00:00 | Close: 461.36180216471354
    Time: 2014-06-01 00:00:00+00:00 | Close: 486.6520031344506
    Time: 2014-07-01 00:00:00+00:00 | Close: 615.916737874349
    Time: 2014-08-01 00:00:00+00:00 | Close: 618.0250637915826
    Time: 2014-09-01 00:00:00+00:00 | Close: 536.0873924993699
    Time: 2014-10-01 00:00:00+00:00 | Close: 445.1866007486979
    Time: 2014-11-01 00:00:00+00:00 | Close: 364.1488726215978
    Time: 2014-12-01 00:00:00+00:00 | Close: 366.09979858398435
    Time: 2015-01-01 00:00:00+00:00 | Close: 341.2678705030872
    Time: 2015-02-01 00:00:00+00:00 | Close: 248.78254748928933
    Time: 2015-03-01 00:00:00+00:00 | Close: 234.15364456176758
    Time: 2015-04-01 00:00:00+00:00 | Close: 269.0422589701991
    Time: 2015-05-01 00:00:00+00:00 | Close: 235.4915339152018
    Time: 2015-06-01 00:00:00+00:00 | Close: 236.9970009096207
    Time: 2015-07-01 00:00:00+00:00 | Close: 238.0817657470703
    Time: 2015-08-01 00:00:00+00:00 | Close: 279.5637398996661
    Time: 2015-09-01 00:00:00+00:00 | Close: 250.73380501039566
    Time: 2015-10-01 00:00:00+00:00 | Close: 233.5955332438151
    Time: 2015-11-01 00:00:00+00:00 | Close: 264.85535553962956
    Time: 2015-12-01 00:00:00+00:00 | Close: 348.8833323160807
    Time: 2016-01-01 00:00:00+00:00 | Close: 424.4645474341608
    Time: 2016-02-01 00:00:00+00:00 | Close: 410.84448537518904
    Time: 2016-03-01 00:00:00+00:00 | Close: 404.4082736311288
    Time: 2016-04-01 00:00:00+00:00 | Close: 416.5257735713836
    Time: 2016-05-01 00:00:00+00:00 | Close: 434.3393981933594
    Time: 2016-06-01 00:00:00+00:00 | Close: 461.9544146137853
    Time: 2016-07-01 00:00:00+00:00 | Close: 642.8690612792968
    Time: 2016-08-01 00:00:00+00:00 | Close: 661.3561027280746
    Time: 2016-09-01 00:00:00+00:00 | Close: 579.585197202621
    Time: 2016-10-01 00:00:00+00:00 | Close: 605.8486328125
    Time: 2016-11-01 00:00:00+00:00 | Close: 643.5509348223286
    Time: 2016-12-01 00:00:00+00:00 | Close: 726.3491007486979
    Time: 2017-01-01 00:00:00+00:00 | Close: 828.0603558940272
    Time: 2017-02-01 00:00:00+00:00 | Close: 914.9161593529486
    Time: 2017-03-01 00:00:00+00:00 | Close: 1062.533671787807
    Time: 2017-04-01 00:00:00+00:00 | Close: 1129.365228468372
    Time: 2017-05-01 00:00:00+00:00 | Close: 1206.641007486979
    Time: 2017-06-01 00:00:00+00:00 | Close: 1895.383529170867
    Time: 2017-07-01 00:00:00+00:00 | Close: 2636.204345703125
    Time: 2017-08-01 00:00:00+00:00 | Close: 2519.4183861517135
    Time: 2017-09-01 00:00:00+00:00 | Close: 3880.9899981098793
    Time: 2017-10-01 00:00:00+00:00 | Close: 4064.8363118489583
    Time: 2017-11-01 00:00:00+00:00 | Close: 5360.071604082661
    Time: 2017-12-01 00:00:00+00:00 | Close: 7813.132975260417
    Time: 2018-01-01 00:00:00+00:00 | Close: 15294.270980342742
    Time: 2018-02-01 00:00:00+00:00 | Close: 13085.558089717742
    Time: 2018-03-01 00:00:00+00:00 | Close: 9472.001150948661
    Time: 2018-04-01 00:00:00+00:00 | Close: 9040.557097404233
    Time: 2018-05-01 00:00:00+00:00 | Close: 8033.596630859375
    Time: 2018-06-01 00:00:00+00:00 | Close: 8450.997731854839
    Time: 2018-07-01 00:00:00+00:00 | Close: 6793.507666015625
    Time: 2018-08-01 00:00:00+00:00 | Close: 7146.349989919355
    Time: 2018-09-01 00:00:00+00:00 | Close: 6700.130000000002
    Time: 2018-10-01 00:00:00+00:00 | Close: 6610.675000000001
    Time: 2018-11-01 00:00:00+00:00 | Close: 6485.118709677419
    Time: 2018-12-01 00:00:00+00:00 | Close: 5404.250163745335
    Time: 2019-01-01 00:00:00+00:00 | Close: 3717.4883192654843
    Time: 2019-02-01 00:00:00+00:00 | Close: 3701.5549733116122
    Time: 2019-03-01 00:00:00+00:00 | Close: 3711.907275630714
    Time: 2019-04-01 00:00:00+00:00 | Close: 3976.0690934074196
    Time: 2019-05-01 00:00:00+00:00 | Close: 5178.469425008667
    Time: 2019-06-01 00:00:00+00:00 | Close: 7309.694113368711
    Time: 2019-07-01 00:00:00+00:00 | Close: 9415.900143546
    Time: 2019-08-01 00:00:00+00:00 | Close: 10669.33622277516
    Time: 2019-09-01 00:00:00+00:00 | Close: 10643.24839313613
    Time: 2019-10-01 00:00:00+00:00 | Close: 9814.067782100668
    Time: 2019-11-01 00:00:00+00:00 | Close: 8411.929149071937
    Time: 2019-12-01 00:00:00+00:00 | Close: 8373.572452042665
    Time: 2020-01-01 00:00:00+00:00 | Close: 7284.0130458951635
    Time: 2020-02-01 00:00:00+00:00 | Close: 8389.270450449678
    Time: 2020-03-01 00:00:00+00:00 | Close: 9630.722210922067
    Time: 2020-04-01 00:00:00+00:00 | Close: 6871.016110927743
    Time: 2020-05-01 00:00:00+00:00 | Close: 7224.477345241333
    Time: 2020-06-01 00:00:00+00:00 | Close: 9263.151880502257
    Time: 2020-07-01 00:00:00+00:00 | Close: 9489.227163164333
    Time: 2020-08-01 00:00:00+00:00 | Close: 9589.899754957421
    Time: 2020-09-01 00:00:00+00:00 | Close: 11652.394214906453
    Time: 2020-10-01 00:00:00+00:00 | Close: 10660.276814935667
    Time: 2020-11-01 00:00:00+00:00 | Close: 11886.978148203545
    Time: 2020-12-01 00:00:00+00:00 | Close: 16645.757397035995
    Time: 2021-01-01 00:00:00+00:00 | Close: 21983.13691412839
    Time: 2021-02-01 00:00:00+00:00 | Close: 34761.6498821042
    Time: 2021-03-01 00:00:00+00:00 | Close: 46306.798799221775
    Time: 2021-04-01 00:00:00+00:00 | Close: 54998.00857016419
    Time: 2021-05-01 00:00:00+00:00 | Close: 57206.72022674067
    Time: 2021-06-01 00:00:00+00:00 | Close: 46443.28605283192
    Time: 2021-07-01 00:00:00+00:00 | Close: 35845.15485565401
    Time: 2021-08-01 00:00:00+00:00 | Close: 34234.44838624
    --- Conexión Cerrada ---


![imagen.png](e1bc016d-4a4f-4260-afc8-9c00a25c39ba.png)

### **Tarea 2.2: Rango de volatilidad**

Calcula el precio máximo y mínimo por semana para la criptomoneda **``Stellar``**.

1. Filtra los precios de cierre de **``XLM``** del **año 2019**.
2. Usa ``aggregateWindow()`` dos veces (o una vez con dos funciones):
- Una pipeline para calcular el **máximo semanal** (``fn: max``, ``every: 1wk``).
- Una pipeline para calcular el **mínimo semanal** (``fn: min``, ``every: 1wk``).
3. Usa ``yield()`` para emitir ambos resultados.


```python
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point

INFLUX_URL = "http://influxdb-influxdb2-1:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="

print("--- Iniciando conexión a InfluxDB ---")

client = None

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org="docs"
        )
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    health = client.health()
    
    if health.status == "pass":
        print("[INFO] ¡Conexión Exitosa!")
        print(f"[INFO] Versión del servidor: {health.version}")
        ##Aqui va la logica
        tarea = """
from(bucket: "crypto_raw")
  |> range(start: 2019-01-01T00:00:00Z, stop: 2019-12-31T23:59:59Z)
  |> filter(fn: (r) => r._measurement == "daily_quotes")
  |> filter(fn: (r) => r._field == "close")
  |> filter(fn: (r) => r.symbol == "XLM")
  |> aggregateWindow(every: 1w, fn: max, createEmpty: false)
  |> yield(name: "weekly_max")

from(bucket: "crypto_raw")
  |> range(start: 2019-01-01T00:00:00Z, stop: 2019-12-31T23:59:59Z)
  |> filter(fn: (r) => r._measurement == "daily_quotes")
  |> filter(fn: (r) => r._field == "close")
  |> filter(fn: (r) => r.symbol == "XLM")
  |> aggregateWindow(every: 1w, fn: min, createEmpty: false)
  |> yield(name: "weekly_min")
        """
        query_api = client.query_api()

        print("[INFO] Ejecutando consulta")
        tables = query_api.query(query=tarea, org="docs")
        
        for table in tables:
            for record in table.records:
                print(
                    f"Time: {record.get_time()} | "
                    f"Close: {record.get_value()}"
                )
    
    else:
        print(f"[Error] Conexion fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")
except (InfluxDBError,NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f" Detalle: {e}")
finally:
    if client:
        client.close()
        print("--- Conexión Cerrada ---")
```

    --- Iniciando conexión a InfluxDB ---
    Verificando estado de salud de InfluxDB en http://influxdb-influxdb2-1:8086
    [INFO] ¡Conexión Exitosa!
    [INFO] Versión del servidor: v2.7.12
    [INFO] Ejecutando consulta
    Time: 2019-01-03 00:00:00+00:00 | Close: 0.11593003965
    Time: 2019-01-10 00:00:00+00:00 | Close: 0.113824645405
    Time: 2019-01-17 00:00:00+00:00 | Close: 0.103608750666
    Time: 2019-01-24 00:00:00+00:00 | Close: 0.102576372742
    Time: 2019-01-31 00:00:00+00:00 | Close: 0.0839227197999
    Time: 2019-02-07 00:00:00+00:00 | Close: 0.0743873347098
    Time: 2019-02-14 00:00:00+00:00 | Close: 0.0746880850898
    Time: 2019-02-21 00:00:00+00:00 | Close: 0.076635145311
    Time: 2019-02-28 00:00:00+00:00 | Close: 0.0842337176392
    Time: 2019-03-07 00:00:00+00:00 | Close: 0.0835385127758
    Time: 2019-03-14 00:00:00+00:00 | Close: 0.0855406472047
    Time: 2019-03-21 00:00:00+00:00 | Close: 0.107271925309
    Time: 2019-03-28 00:00:00+00:00 | Close: 0.102469191942
    Time: 2019-04-04 00:00:00+00:00 | Close: 0.107359387845
    Time: 2019-04-11 00:00:00+00:00 | Close: 0.11878829353
    Time: 2019-04-18 00:00:00+00:00 | Close: 0.113628616719
    Time: 2019-04-25 00:00:00+00:00 | Close: 0.103259281028
    Time: 2019-05-02 00:00:00+00:00 | Close: 0.0964745129392
    Time: 2019-05-09 00:00:00+00:00 | Close: 0.0936971600069
    Time: 2019-05-16 00:00:00+00:00 | Close: 0.0902320403193
    Time: 2019-05-23 00:00:00+00:00 | Close: 0.124257250797
    Time: 2019-05-30 00:00:00+00:00 | Close: 0.125166646196
    Time: 2019-06-06 00:00:00+00:00 | Close: 0.121283780398
    Time: 2019-06-13 00:00:00+00:00 | Close: 0.119915400277
    Time: 2019-06-20 00:00:00+00:00 | Close: 0.124301592251
    Time: 2019-06-27 00:00:00+00:00 | Close: 0.12150678527
    Time: 2019-07-04 00:00:00+00:00 | Close: 0.103390157874
    Time: 2019-07-11 00:00:00+00:00 | Close: 0.0950565703023
    Time: 2019-07-18 00:00:00+00:00 | Close: 0.0783180471619
    Time: 2019-07-25 00:00:00+00:00 | Close: 0.084467858308
    Time: 2019-08-01 00:00:00+00:00 | Close: 0.083512564551
    Time: 2019-08-08 00:00:00+00:00 | Close: 0.0782121757967
    Time: 2019-08-15 00:00:00+00:00 | Close: 0.0691830893629
    Time: 2019-08-22 00:00:00+00:00 | Close: 0.0676973150428
    Time: 2019-08-29 00:00:00+00:00 | Close: 0.0661375592649
    Time: 2019-09-05 00:00:00+00:00 | Close: 0.0621784173174
    Time: 2019-09-12 00:00:00+00:00 | Close: 0.0583726083727
    Time: 2019-09-19 00:00:00+00:00 | Close: 0.0569399656847
    Time: 2019-09-26 00:00:00+00:00 | Close: 0.0545038067121
    Time: 2019-10-03 00:00:00+00:00 | Close: 0.0581272753922
    Time: 2019-10-10 00:00:00+00:00 | Close: 0.0588752275909
    Time: 2019-10-17 00:00:00+00:00 | Close: 0.0596294085884
    Time: 2019-10-24 00:00:00+00:00 | Close: 0.0599839569322
    Time: 2019-10-31 00:00:00+00:00 | Close: 0.0606116062591
    Time: 2019-11-07 00:00:00+00:00 | Close: 0.0652148662313
    Time: 2019-11-14 00:00:00+00:00 | Close: 0.071887807681
    Time: 2019-11-21 00:00:00+00:00 | Close: 0.0655019886487
    Time: 2019-11-28 00:00:00+00:00 | Close: 0.0568813691786
    Time: 2019-12-05 00:00:00+00:00 | Close: 0.0554190238714
    Time: 2019-12-12 00:00:00+00:00 | Close: 0.0526917948915
    Time: 2019-12-19 00:00:00+00:00 | Close: 0.0440530520227
    Time: 2019-12-26 00:00:00+00:00 | Close: 0.0434406551581
    Time: 2019-12-31 23:59:59+00:00 | Close: 0.0451006564413
    Time: 2019-01-03 00:00:00+00:00 | Close: 0.119331410154
    Time: 2019-01-10 00:00:00+00:00 | Close: 0.123774386729
    Time: 2019-01-17 00:00:00+00:00 | Close: 0.109878610051
    Time: 2019-01-24 00:00:00+00:00 | Close: 0.108460938657
    Time: 2019-01-31 00:00:00+00:00 | Close: 0.102210392352
    Time: 2019-02-07 00:00:00+00:00 | Close: 0.0835802499476
    Time: 2019-02-14 00:00:00+00:00 | Close: 0.081224003372
    Time: 2019-02-21 00:00:00+00:00 | Close: 0.0917350058181
    Time: 2019-02-28 00:00:00+00:00 | Close: 0.0942568445555
    Time: 2019-03-07 00:00:00+00:00 | Close: 0.0872353323243
    Time: 2019-03-14 00:00:00+00:00 | Close: 0.108198619481
    Time: 2019-03-21 00:00:00+00:00 | Close: 0.115914392752
    Time: 2019-03-28 00:00:00+00:00 | Close: 0.108692806617
    Time: 2019-04-04 00:00:00+00:00 | Close: 0.121900837603
    Time: 2019-04-11 00:00:00+00:00 | Close: 0.131995967869
    Time: 2019-04-18 00:00:00+00:00 | Close: 0.117505252017
    Time: 2019-04-25 00:00:00+00:00 | Close: 0.117362975895
    Time: 2019-05-02 00:00:00+00:00 | Close: 0.101351137089
    Time: 2019-05-09 00:00:00+00:00 | Close: 0.102295013854
    Time: 2019-05-16 00:00:00+00:00 | Close: 0.137001655066
    Time: 2019-05-23 00:00:00+00:00 | Close: 0.141485197931
    Time: 2019-05-30 00:00:00+00:00 | Close: 0.138959876059
    Time: 2019-06-06 00:00:00+00:00 | Close: 0.137622959913
    Time: 2019-06-13 00:00:00+00:00 | Close: 0.127541536282
    Time: 2019-06-20 00:00:00+00:00 | Close: 0.131035168284
    Time: 2019-06-27 00:00:00+00:00 | Close: 0.129050324633
    Time: 2019-07-04 00:00:00+00:00 | Close: 0.114503902451
    Time: 2019-07-11 00:00:00+00:00 | Close: 0.105053888576
    Time: 2019-07-18 00:00:00+00:00 | Close: 0.0979634554654
    Time: 2019-07-25 00:00:00+00:00 | Close: 0.0951105058824
    Time: 2019-08-01 00:00:00+00:00 | Close: 0.0879653185781
    Time: 2019-08-08 00:00:00+00:00 | Close: 0.0830260889325
    Time: 2019-08-15 00:00:00+00:00 | Close: 0.077841261029
    Time: 2019-08-22 00:00:00+00:00 | Close: 0.0717945667003
    Time: 2019-08-29 00:00:00+00:00 | Close: 0.0716762386253
    Time: 2019-09-05 00:00:00+00:00 | Close: 0.063233045025
    Time: 2019-09-12 00:00:00+00:00 | Close: 0.0608816630268
    Time: 2019-09-19 00:00:00+00:00 | Close: 0.0831183072597
    Time: 2019-09-26 00:00:00+00:00 | Close: 0.0813871907299
    Time: 2019-10-03 00:00:00+00:00 | Close: 0.0614401007616
    Time: 2019-10-10 00:00:00+00:00 | Close: 0.0633552899625
    Time: 2019-10-17 00:00:00+00:00 | Close: 0.064924881188
    Time: 2019-10-24 00:00:00+00:00 | Close: 0.0645472454791
    Time: 2019-10-31 00:00:00+00:00 | Close: 0.0661851181536
    Time: 2019-11-07 00:00:00+00:00 | Close: 0.082164007855
    Time: 2019-11-14 00:00:00+00:00 | Close: 0.0798086163683
    Time: 2019-11-21 00:00:00+00:00 | Close: 0.074740405351
    Time: 2019-11-28 00:00:00+00:00 | Close: 0.0616827581745
    Time: 2019-12-05 00:00:00+00:00 | Close: 0.0596409680538
    Time: 2019-12-12 00:00:00+00:00 | Close: 0.0561321294528
    Time: 2019-12-19 00:00:00+00:00 | Close: 0.0529900639054
    Time: 2019-12-26 00:00:00+00:00 | Close: 0.0472958798315
    Time: 2019-12-31 23:59:59+00:00 | Close: 0.0462155943798
    --- Conexión Cerrada ---


![imagen.png](8d454cf7-0a6e-414e-bf5b-c22e9bfb9672.png)


## **PARTE III: Manipulación y Joins**

Estas tareas requieren transformar los datos o combinar información de diferentes series de tiempo.

### **Tarea 3.1: Cálculo de variación porcentual diaria (Map)**

Escribe una consulta que:
1. Filtre los precios de cierre (``close``) de **Tether ()**``USDT``) de los **años 2016 a 2018**.
2. Usa la función **``difference()``** para obtener la diferencia absoluta (en dólares) entre los precios de cierre diarios.
3. Usa la función **``map()``** para transformar el resultado anterior y calcular la **variación porcentual diaria** (Diferencia / Precio del día anterior).


```python
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point

INFLUX_URL = "http://influxdb-influxdb2-1:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="

print("--- Iniciando conexión a InfluxDB ---")

client = None

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org="docs"
        )
    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    health = client.health()
    
    if health.status == "pass":
        print("[INFO] ¡Conexión Exitosa!")
        print(f"[INFO] Versión del servidor: {health.version}")
        ##Aqui va la logica
        tarea = """
from(bucket: "crypto_raw")
  |> range(start: 2016-01-01T00:00:00Z, stop: 2018-12-31T23:59:59Z)
  |> filter(fn: (r) => r._measurement == "daily_quotes")
  |> filter(fn: (r) => r._field == "close")
  |> filter(fn: (r) => r.name == "Tether")
  |> sort(columns: ["_time"])
  |> difference(nonNegative: false)
  |> map(fn: (r) => ({
      r with
      pct_change: r._value / (r._value + r._difference)
  }))
        """
        query_api = client.query_api()

        print("[INFO] Ejecutando consulta")
        tables = query_api.query(query=tarea, org="docs")
        
        for table in tables:
            for record in table.records:
                print(
                    f"Time: {record.get_time()} | "
                    f"Close: {record.get_value()}"
                )
    
    else:
        print(f"[Error] Conexion fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")
except (InfluxDBError,NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f" Detalle: {e}")
finally:
    if client:
        client.close()
        print("--- Conexión Cerrada ---")
```

    --- Iniciando conexión a InfluxDB ---
    Verificando estado de salud de InfluxDB en http://influxdb-influxdb2-1:8086
    [INFO] ¡Conexión Exitosa!
    [INFO] Versión del servidor: v2.7.12
    [INFO] Ejecutando consulta
    Time: 2016-01-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-05 23:59:59+00:00 | Close: 0.0002499818801879883
    Time: 2016-01-06 23:59:59+00:00 | Close: -0.0002499818801879883
    Time: 2016-01-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-13 23:59:59+00:00 | Close: 0.0004500150680541992
    Time: 2016-01-14 23:59:59+00:00 | Close: -0.0004500150680541992
    Time: 2016-01-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-16 23:59:59+00:00 | Close: 0.0004099607467651367
    Time: 2016-01-17 23:59:59+00:00 | Close: -0.0004099607467651367
    Time: 2016-01-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-22 23:59:59+00:00 | Close: 6.99758529663086e-05
    Time: 2016-01-23 23:59:59+00:00 | Close: 7.998943328857422e-05
    Time: 2016-01-24 23:59:59+00:00 | Close: -0.0001399517059326172
    Time: 2016-01-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-26 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2016-01-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-01-28 23:59:59+00:00 | Close: -1.0132789611816406e-06
    Time: 2016-01-29 23:59:59+00:00 | Close: -2.09808349609375e-05
    Time: 2016-01-30 23:59:59+00:00 | Close: 2.199411392211914e-05
    Time: 2016-01-31 23:59:59+00:00 | Close: -1.0132789611816406e-06
    Time: 2016-02-01 23:59:59+00:00 | Close: -2.9981136322021484e-05
    Time: 2016-02-02 23:59:59+00:00 | Close: 3.0994415283203125e-05
    Time: 2016-02-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-14 23:59:59+00:00 | Close: 0.0008900165557861328
    Time: 2016-02-15 23:59:59+00:00 | Close: -0.0008800029754638672
    Time: 2016-02-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-17 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2016-02-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-24 23:59:59+00:00 | Close: -0.00015598535537719727
    Time: 2016-02-25 23:59:59+00:00 | Close: 0.00015598535537719727
    Time: 2016-02-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-02-29 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2016-03-01 23:59:59+00:00 | Close: -2.9027462005615234e-05
    Time: 2016-03-02 23:59:59+00:00 | Close: -2.9027462005615234e-05
    Time: 2016-03-03 23:59:59+00:00 | Close: 3.701448440551758e-05
    Time: 2016-03-04 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-03-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-06 23:59:59+00:00 | Close: -2.0265579223632812e-06
    Time: 2016-03-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-08 23:59:59+00:00 | Close: 2.0265579223632812e-06
    Time: 2016-03-09 23:59:59+00:00 | Close: -0.00010502338409423828
    Time: 2016-03-10 23:59:59+00:00 | Close: 9.900331497192383e-05
    Time: 2016-03-11 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-03-12 23:59:59+00:00 | Close: -0.00010001659393310547
    Time: 2016-03-13 23:59:59+00:00 | Close: 2.300739288330078e-05
    Time: 2016-03-14 23:59:59+00:00 | Close: 7.599592208862305e-05
    Time: 2016-03-15 23:59:59+00:00 | Close: 6.020069122314453e-06
    Time: 2016-03-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-17 23:59:59+00:00 | Close: -1.6987323760986328e-05
    Time: 2016-03-18 23:59:59+00:00 | Close: 1.4960765838623047e-05
    Time: 2016-03-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-21 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-03-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-24 23:59:59+00:00 | Close: -2.7000904083251953e-05
    Time: 2016-03-25 23:59:59+00:00 | Close: 2.8014183044433594e-05
    Time: 2016-03-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-03-31 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-06 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2016-04-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-08 23:59:59+00:00 | Close: -2.002716064453125e-05
    Time: 2016-04-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-11 23:59:59+00:00 | Close: -0.00013899803161621094
    Time: 2016-04-12 23:59:59+00:00 | Close: 0.00013899803161621094
    Time: 2016-04-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-14 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-24 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-04-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-13 23:59:59+00:00 | Close: 0.003260016441345215
    Time: 2016-05-14 23:59:59+00:00 | Close: 0.0003199577331542969
    Time: 2016-05-15 23:59:59+00:00 | Close: -0.0035799741744995117
    Time: 2016-05-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-24 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2016-05-25 23:59:59+00:00 | Close: -2.002716064453125e-05
    Time: 2016-05-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-05-31 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-14 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-16 23:59:59+00:00 | Close: -1.0132789611816406e-06
    Time: 2016-06-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-20 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-06-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-24 23:59:59+00:00 | Close: 1.0013580322265625e-05
    Time: 2016-06-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-27 23:59:59+00:00 | Close: -5.900859832763672e-05
    Time: 2016-06-28 23:59:59+00:00 | Close: 4.8995018005371094e-05
    Time: 2016-06-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-06-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-07 23:59:59+00:00 | Close: -9.000301361083984e-06
    Time: 2016-07-08 23:59:59+00:00 | Close: 7.987022399902344e-06
    Time: 2016-07-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-11 23:59:59+00:00 | Close: 0.00016099214553833008
    Time: 2016-07-12 23:59:59+00:00 | Close: -0.00015997886657714844
    Time: 2016-07-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-14 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-19 23:59:59+00:00 | Close: 1.0013580322265625e-05
    Time: 2016-07-20 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2016-07-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-24 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-25 23:59:59+00:00 | Close: -1.0132789611816406e-06
    Time: 2016-07-26 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-07-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-07-29 23:59:59+00:00 | Close: 7.998943328857422e-05
    Time: 2016-07-30 23:59:59+00:00 | Close: -6.99758529663086e-05
    Time: 2016-07-31 23:59:59+00:00 | Close: -4.70280647277832e-05
    Time: 2016-08-01 23:59:59+00:00 | Close: 3.600120544433594e-05
    Time: 2016-08-02 23:59:59+00:00 | Close: -3.993511199951172e-06
    Time: 2016-08-03 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-08-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-05 23:59:59+00:00 | Close: -0.00016301870346069336
    Time: 2016-08-06 23:59:59+00:00 | Close: -0.0002759695053100586
    Time: 2016-08-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-10 23:59:59+00:00 | Close: -0.025997042655944824
    Time: 2016-08-11 23:59:59+00:00 | Close: -0.011184990406036377
    Time: 2016-08-12 23:59:59+00:00 | Close: -0.00031697750091552734
    Time: 2016-08-13 23:59:59+00:00 | Close: 0.03794097900390625
    Time: 2016-08-14 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-16 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-08-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-24 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-08-31 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-12 23:59:59+00:00 | Close: 0.0006999969482421875
    Time: 2016-09-13 23:59:59+00:00 | Close: -0.0006899833679199219
    Time: 2016-09-14 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2016-09-15 23:59:59+00:00 | Close: -6.973743438720703e-06
    Time: 2016-09-16 23:59:59+00:00 | Close: 5.9604644775390625e-06
    Time: 2016-09-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-18 23:59:59+00:00 | Close: -7.599592208862305e-05
    Time: 2016-09-19 23:59:59+00:00 | Close: 7.599592208862305e-05
    Time: 2016-09-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-21 23:59:59+00:00 | Close: -1.0967254638671875e-05
    Time: 2016-09-22 23:59:59+00:00 | Close: 1.0967254638671875e-05
    Time: 2016-09-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-24 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-25 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-09-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-09-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-02 23:59:59+00:00 | Close: -2.0265579223632812e-06
    Time: 2016-10-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-04 23:59:59+00:00 | Close: 2.0265579223632812e-06
    Time: 2016-10-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-14 23:59:59+00:00 | Close: -1.0132789611816406e-06
    Time: 2016-10-15 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2016-10-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-24 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-10-31 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-03 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-04 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-05 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-06 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-10 23:59:59+00:00 | Close: -2.9802322387695312e-06
    Time: 2016-11-11 23:59:59+00:00 | Close: 2.9802322387695312e-06
    Time: 2016-11-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-14 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-16 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-18 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-19 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-23 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-24 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-28 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-29 23:59:59+00:00 | Close: 0.0
    Time: 2016-11-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-01 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-02 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-03 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2016-12-04 23:59:59+00:00 | Close: 0.00015997886657714844
    Time: 2016-12-05 23:59:59+00:00 | Close: -0.00015997886657714844
    Time: 2016-12-06 23:59:59+00:00 | Close: -2.002716064453125e-05
    Time: 2016-12-07 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-08 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-09 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-10 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-11 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-12 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-13 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-14 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-15 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-16 23:59:59+00:00 | Close: 3.0040740966796875e-05
    Time: 2016-12-17 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-18 23:59:59+00:00 | Close: -2.002716064453125e-05
    Time: 2016-12-19 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2016-12-20 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-21 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-22 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-23 23:59:59+00:00 | Close: 0.00016999244689941406
    Time: 2016-12-24 23:59:59+00:00 | Close: -0.00015997886657714844
    Time: 2016-12-25 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-26 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-27 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-28 23:59:59+00:00 | Close: 3.0040740966796875e-05
    Time: 2016-12-29 23:59:59+00:00 | Close: -2.002716064453125e-05
    Time: 2016-12-30 23:59:59+00:00 | Close: 0.0
    Time: 2016-12-31 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2017-01-01 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-02 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-03 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-04 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-05 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-06 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-07 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-08 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-09 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-10 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-11 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-12 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-13 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-14 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2017-01-15 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2017-01-16 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2017-01-17 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-18 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-19 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-20 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-21 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-22 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-23 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-24 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-25 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-26 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-27 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-28 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-29 23:59:59+00:00 | Close: 0.0
    Time: 2017-01-30 23:59:59+00:00 | Close: 0.00030994415283203125
    Time: 2017-01-31 23:59:59+00:00 | Close: -0.0003229379653930664
    Time: 2017-02-01 23:59:59+00:00 | Close: 1.9669532775878906e-06
    Time: 2017-02-02 23:59:59+00:00 | Close: -5.0067901611328125e-06
    Time: 2017-02-03 23:59:59+00:00 | Close: 3.993511199951172e-06
    Time: 2017-02-04 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2017-02-05 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-06 23:59:59+00:00 | Close: -1.0132789611816406e-06
    Time: 2017-02-07 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2017-02-08 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-09 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-10 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-11 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-12 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-13 23:59:59+00:00 | Close: 1.0132789611816406e-06
    Time: 2017-02-14 23:59:59+00:00 | Close: 0.0
    Time: 2017-02-15 23:59:59+00:00 | Close: 0.00177001953125
    Time: 2017-02-16 23:59:59+00:00 | Close: -0.0017200708389282227
    Time: 2017-02-17 23:59:59+00:00 | Close: -2.9921531677246094e-05
    Time: 2017-02-18 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2017-02-19 23:59:59+00:00 | Close: -0.00011199712753295898
    Time: 2017-02-20 23:59:59+00:00 | Close: 9.900331497192383e-05
    Time: 2017-02-21 23:59:59+00:00 | Close: -0.00023704767227172852
    Time: 2017-02-22 23:59:59+00:00 | Close: 0.00020700693130493164
    Time: 2017-02-23 23:59:59+00:00 | Close: 3.0040740966796875e-05
    Time: 2017-02-24 23:59:59+00:00 | Close: 9.5367431640625e-07
    Time: 2017-02-25 23:59:59+00:00 | Close: 4.208087921142578e-05
    Time: 2017-02-26 23:59:59+00:00 | Close: -3.0040740966796875e-05
    Time: 2017-02-27 23:59:59+00:00 | Close: 5.996227264404297e-05
    Time: 2017-02-28 23:59:59+00:00 | Close: -9.995698928833008e-05
    Time: 2017-03-01 23:59:59+00:00 | Close: 2.7954578399658203e-05
    Time: 2017-03-02 23:59:59+00:00 | Close: 2.0265579223632812e-06
    Time: 2017-03-03 23:59:59+00:00 | Close: 0.0
    Time: 2017-03-04 23:59:59+00:00 | Close: 1.0013580322265625e-05
    Time: 2017-03-05 23:59:59+00:00 | Close: 0.0
    Time: 2017-03-06 23:59:59+00:00 | Close: 4.9948692321777344e-05
    Time: 2017-03-07 23:59:59+00:00 | Close: -3.993511199951172e-05
    Time: 2017-03-08 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2017-03-09 23:59:59+00:00 | Close: -0.00010401010513305664
    Time: 2017-03-10 23:59:59+00:00 | Close: 8.398294448852539e-05
    Time: 2017-03-11 23:59:59+00:00 | Close: 5.0067901611328125e-05
    Time: 2017-03-12 23:59:59+00:00 | Close: 3.993511199951172e-05
    Time: 2017-03-13 23:59:59+00:00 | Close: -3.993511199951172e-05
    Time: 2017-03-14 23:59:59+00:00 | Close: -2.002716064453125e-05
    Time: 2017-03-15 23:59:59+00:00 | Close: -1.0013580322265625e-05
    Time: 2017-03-16 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2017-03-17 23:59:59+00:00 | Close: 0.0
    Time: 2017-03-18 23:59:59+00:00 | Close: 0.0
    Time: 2017-03-19 23:59:59+00:00 | Close: 1.990795135498047e-05
    Time: 2017-03-20 23:59:59+00:00 | Close: 0.00016009807586669922
    Time: 2017-03-21 23:59:59+00:00 | Close: -0.0001800060272216797
    Time: 2017-03-22 23:59:59+00:00 | Close: 1.0013580322265625e-05
    Time: 2017-03-23 23:59:59+00:00 | Close: 2.9921531677246094e-05
    Time: 2017-03-24 23:59:59+00:00 | Close: -0.00017398595809936523
    Time: 2017-03-25 23:59:59+00:00 | Close: 2.002716064453125e-05
    Time: 2017-03-26 23:59:59+00:00 | Close: 9.399652481079102e-05
    Time: 2017-03-27 23:59:59+00:00 | Close: 0.0
    Time: 2017-03-28 23:59:59+00:00 | Close: 0.0
    Time: 2017-03-29 23:59:59+00:00 | Close: -6.300210952758789e-05
    Time: 2017-03-30 23:59:59+00:00 | Close: 3.898143768310547e-05
    Time: 2017-03-31 23:59:59+00:00 | Close: 1.4007091522216797e-05
    Time: 2017-04-01 23:59:59+00:00 | Close: -0.0004140138626098633
    Time: 2017-04-02 23:59:59+00:00 | Close: 0.001363992691040039
    Time: 2017-04-03 23:59:59+00:00 | Close: -0.0011979937553405762
    Time: 2017-04-04 23:59:59+00:00 | Close: 0.00026804208755493164
    Time: 2017-04-05 23:59:59+00:00 | Close: 9.000301361083984e-05
    Time: 2017-04-06 23:59:59+00:00 | Close: -0.0001710057258605957
    Time: 2017-04-07 23:59:59+00:00 | Close: -6.604194641113281e-05
    Time: 2017-04-08 23:59:59+00:00 | Close: -0.0001569986343383789
    Time: 2017-04-09 23:59:59+00:00 | Close: 0.00024402141571044922
    Time: 2017-04-10 23:59:59+00:00 | Close: -2.9027462005615234e-05
    Time: 2017-04-11 23:59:59+00:00 | Close: -8.797645568847656e-05
    Time: 2017-04-12 23:59:59+00:00 | Close: -0.0002809762954711914
    Time: 2017-04-13 23:59:59+00:00 | Close: 4.9948692321777344e-05
    Time: 2017-04-14 23:59:59+00:00 | Close: -0.0006259679794311523
    Time: 2017-04-15 23:59:59+00:00 | Close: 0.0009530186653137207
    Time: 2017-04-16 23:59:59+00:00 | Close: -0.00048100948333740234
    Time: 2017-04-17 23:59:59+00:00 | Close: -0.00016999244689941406
    Time: 2017-04-18 23:59:59+00:00 | Close: 0.0003280043601989746
    Time: 2017-04-19 23:59:59+00:00 | Close: -9.304285049438477e-05
    Time: 2017-04-20 23:59:59+00:00 | Close: -0.001248002052307129
    Time: 2017-04-21 23:59:59+00:00 | Close: -0.01410597562789917
    Time: 2017-04-22 23:59:59+00:00 | Close: -0.0432400107383728
    Time: 2017-04-23 23:59:59+00:00 | Close: -0.019595980644226074
    Time: 2017-04-24 23:59:59+00:00 | Close: -0.003443002700805664
    Time: 2017-04-25 23:59:59+00:00 | Close: -0.004294991493225098
    Time: 2017-04-26 23:59:59+00:00 | Close: 0.007454991340637207
    Time: 2017-04-27 23:59:59+00:00 | Close: 0.003300964832305908
    Time: 2017-04-28 23:59:59+00:00 | Close: 0.010191023349761963
    Time: 2017-04-29 23:59:59+00:00 | Close: 0.0026509761810302734
    Time: 2017-04-30 23:59:59+00:00 | Close: -0.0003389716148376465
    Time: 2017-05-01 23:59:59+00:00 | Close: -0.0009829998016357422
    Time: 2017-05-02 23:59:59+00:00 | Close: -0.003264009952545166
    Time: 2017-05-03 23:59:59+00:00 | Close: 0.0007439851760864258
    Time: 2017-05-04 23:59:59+00:00 | Close: 0.012580037117004395
    Time: 2017-05-05 23:59:59+00:00 | Close: 0.009669959545135498
    Time: 2017-05-06 23:59:59+00:00 | Close: 0.013018012046813965
    Time: 2017-05-07 23:59:59+00:00 | Close: 0.00037103891372680664
    Time: 2017-05-08 23:59:59+00:00 | Close: -0.0017300248146057129
    Time: 2017-05-09 23:59:59+00:00 | Close: 0.0032269954681396484
    Time: 2017-05-10 23:59:59+00:00 | Close: 0.011512994766235352
    Time: 2017-05-11 23:59:59+00:00 | Close: 0.001721024513244629
    Time: 2017-05-12 23:59:59+00:00 | Close: -0.007651031017303467
    Time: 2017-05-13 23:59:59+00:00 | Close: -0.0024219751358032227
    Time: 2017-05-14 23:59:59+00:00 | Close: 0.0074579715728759766
    Time: 2017-05-15 23:59:59+00:00 | Close: -0.013808012008666992
    Time: 2017-05-16 23:59:59+00:00 | Close: -0.008706986904144287
    Time: 2017-05-17 23:59:59+00:00 | Close: 0.011838018894195557
    Time: 2017-05-18 23:59:59+00:00 | Close: -0.003286004066467285
    Time: 2017-05-19 23:59:59+00:00 | Close: 0.03405696153640747
    Time: 2017-05-20 23:59:59+00:00 | Close: -0.007768988609313965
    Time: 2017-05-21 23:59:59+00:00 | Close: 0.006649017333984375
    Time: 2017-05-22 23:59:59+00:00 | Close: 0.007779955863952637
    Time: 2017-05-23 23:59:59+00:00 | Close: -0.0015599727630615234
    Time: 2017-05-24 23:59:59+00:00 | Close: 0.010560035705566406
    Time: 2017-05-25 23:59:59+00:00 | Close: 0.019739985466003418
    Time: 2017-05-26 23:59:59+00:00 | Close: -0.00039005279541015625
    Time: 2017-05-27 23:59:59+00:00 | Close: -0.0125199556350708
    Time: 2017-05-28 23:59:59+00:00 | Close: 0.01875007152557373
    Time: 2017-05-29 23:59:59+00:00 | Close: -0.020840048789978027
    Time: 2017-05-30 23:59:59+00:00 | Close: -0.012089967727661133
    Time: 2017-05-31 23:59:59+00:00 | Close: 0.02676999568939209
    Time: 2017-06-01 23:59:59+00:00 | Close: -0.005710005760192871
    Time: 2017-06-02 23:59:59+00:00 | Close: -0.006690025329589844
    Time: 2017-06-03 23:59:59+00:00 | Close: -0.0006600618362426758
    Time: 2017-06-04 23:59:59+00:00 | Close: -0.01157999038696289
    Time: 2017-06-05 23:59:59+00:00 | Close: 0.005160093307495117
    Time: 2017-06-06 23:59:59+00:00 | Close: -0.011970043182373047
    Time: 2017-06-07 23:59:59+00:00 | Close: 0.004150032997131348
    Time: 2017-06-08 23:59:59+00:00 | Close: -0.004220008850097656
    Time: 2017-06-09 23:59:59+00:00 | Close: -0.004090070724487305
    Time: 2017-06-10 23:59:59+00:00 | Close: 0.02369999885559082
    Time: 2017-06-11 23:59:59+00:00 | Close: -0.016199946403503418
    Time: 2017-06-12 23:59:59+00:00 | Close: 0.0095900297164917
    Time: 2017-06-13 23:59:59+00:00 | Close: -0.009370088577270508
    Time: 2017-06-14 23:59:59+00:00 | Close: 0.016770005226135254
    Time: 2017-06-15 23:59:59+00:00 | Close: -0.007730007171630859
    Time: 2017-06-16 23:59:59+00:00 | Close: -0.0018099546432495117
    Time: 2017-06-17 23:59:59+00:00 | Close: -0.027036011219024658
    Time: 2017-06-18 23:59:59+00:00 | Close: 0.014236032962799072
    Time: 2017-06-19 23:59:59+00:00 | Close: -0.016413986682891846
    Time: 2017-06-20 23:59:59+00:00 | Close: -0.011134028434753418
    Time: 2017-06-21 23:59:59+00:00 | Close: 0.006088972091674805
    Time: 2017-06-22 23:59:59+00:00 | Close: -0.008458971977233887
    Time: 2017-06-23 23:59:59+00:00 | Close: 0.033098042011260986
    Time: 2017-06-24 23:59:59+00:00 | Close: 0.014499902725219727
    Time: 2017-06-25 23:59:59+00:00 | Close: -0.007349967956542969
    Time: 2017-06-26 23:59:59+00:00 | Close: -0.0030499696731567383
    Time: 2017-06-27 23:59:59+00:00 | Close: -0.002969980239868164
    Time: 2017-06-28 23:59:59+00:00 | Close: 0.00466001033782959
    Time: 2017-06-29 23:59:59+00:00 | Close: 0.006009936332702637
    Time: 2017-06-30 23:59:59+00:00 | Close: -0.011969923973083496
    Time: 2017-07-01 23:59:59+00:00 | Close: 0.014140009880065918
    Time: 2017-07-02 23:59:59+00:00 | Close: 0.0002899169921875
    Time: 2017-07-03 23:59:59+00:00 | Close: -0.01951003074645996
    Time: 2017-07-04 23:59:59+00:00 | Close: -0.0019219517707824707
    Time: 2017-07-05 23:59:59+00:00 | Close: -0.0023679733276367188
    Time: 2017-07-06 23:59:59+00:00 | Close: 0.007139980792999268
    Time: 2017-07-07 23:59:59+00:00 | Close: 0.00439000129699707
    Time: 2017-07-08 23:59:59+00:00 | Close: -0.008265018463134766
    Time: 2017-07-09 23:59:59+00:00 | Close: 0.010195016860961914
    Time: 2017-07-10 23:59:59+00:00 | Close: -0.001970052719116211
    Time: 2017-07-11 23:59:59+00:00 | Close: 0.004340052604675293
    Time: 2017-07-12 23:59:59+00:00 | Close: -0.014833986759185791
    Time: 2017-07-13 23:59:59+00:00 | Close: 0.006373941898345947
    Time: 2017-07-14 23:59:59+00:00 | Close: -0.0008299350738525391
    Time: 2017-07-15 23:59:59+00:00 | Close: -0.00102996826171875
    Time: 2017-07-16 23:59:59+00:00 | Close: -0.0028090476989746094
    Time: 2017-07-17 23:59:59+00:00 | Close: -0.0022730231285095215
    Time: 2017-07-18 23:59:59+00:00 | Close: 0.0013279914855957031
    Time: 2017-07-19 23:59:59+00:00 | Close: 0.004874050617218018
    Time: 2017-07-20 23:59:59+00:00 | Close: -0.016224026679992676
    Time: 2017-07-21 23:59:59+00:00 | Close: 0.010335981845855713
    Time: 2017-07-22 23:59:59+00:00 | Close: -0.004001975059509277
    Time: 2017-07-23 23:59:59+00:00 | Close: 0.004561007022857666
    Time: 2017-07-24 23:59:59+00:00 | Close: -0.003764033317565918
    Time: 2017-07-25 23:59:59+00:00 | Close: 0.005805015563964844
    Time: 2017-07-26 23:59:59+00:00 | Close: -0.002847015857696533
    Time: 2017-07-27 23:59:59+00:00 | Close: 0.00032001733779907227
    Time: 2017-07-28 23:59:59+00:00 | Close: 0.004665017127990723
    Time: 2017-07-29 23:59:59+00:00 | Close: -0.005321025848388672
    Time: 2017-07-30 23:59:59+00:00 | Close: 0.002249002456665039
    Time: 2017-07-31 23:59:59+00:00 | Close: 0.0020520687103271484
    Time: 2017-08-01 23:59:59+00:00 | Close: -0.0041010379791259766
    Time: 2017-08-02 23:59:59+00:00 | Close: 0.004611015319824219
    Time: 2017-08-03 23:59:59+00:00 | Close: -0.032126009464263916
    Time: 2017-08-04 23:59:59+00:00 | Close: 0.03504592180252075
    Time: 2017-08-05 23:59:59+00:00 | Close: -0.006035923957824707
    Time: 2017-08-06 23:59:59+00:00 | Close: 0.002725958824157715
    Time: 2017-08-07 23:59:59+00:00 | Close: -0.00478595495223999
    Time: 2017-08-08 23:59:59+00:00 | Close: 0.005255997180938721
    Time: 2017-08-09 23:59:59+00:00 | Close: 0.0013499259948730469
    Time: 2017-08-10 23:59:59+00:00 | Close: -0.009868979454040527
    Time: 2017-08-11 23:59:59+00:00 | Close: 0.007899045944213867
    Time: 2017-08-12 23:59:59+00:00 | Close: 0.00023996829986572266
    Time: 2017-08-13 23:59:59+00:00 | Close: -0.0025140047073364258
    Time: 2017-08-14 23:59:59+00:00 | Close: -0.00045299530029296875
    Time: 2017-08-15 23:59:59+00:00 | Close: 0.0033670663833618164
    Time: 2017-08-16 23:59:59+00:00 | Close: -0.0003300905227661133
    Time: 2017-08-17 23:59:59+00:00 | Close: 0.006749987602233887
    Time: 2017-08-18 23:59:59+00:00 | Close: 0.005380034446716309
    Time: 2017-08-19 23:59:59+00:00 | Close: -0.010589957237243652
    Time: 2017-08-20 23:59:59+00:00 | Close: -0.006111025810241699
    Time: 2017-08-21 23:59:59+00:00 | Close: 0.002633988857269287
    Time: 2017-08-22 23:59:59+00:00 | Close: 0.007257044315338135
    Time: 2017-08-23 23:59:59+00:00 | Close: -0.004510045051574707
    Time: 2017-08-24 23:59:59+00:00 | Close: 0.002910017967224121
    Time: 2017-08-25 23:59:59+00:00 | Close: -0.0020600557327270508
    Time: 2017-08-26 23:59:59+00:00 | Close: -0.003927946090698242
    Time: 2017-08-27 23:59:59+00:00 | Close: 0.004008054733276367
    Time: 2017-08-28 23:59:59+00:00 | Close: -0.001880049705505371
    Time: 2017-08-29 23:59:59+00:00 | Close: 0.00046002864837646484
    Time: 2017-08-30 23:59:59+00:00 | Close: -0.0007799863815307617
    Time: 2017-08-31 23:59:59+00:00 | Close: 0.002379894256591797
    Time: 2017-09-01 23:59:59+00:00 | Close: 0.0012500286102294922
    Time: 2017-09-02 23:59:59+00:00 | Close: 0.013509988784790039
    Time: 2017-09-03 23:59:59+00:00 | Close: -0.015649914741516113
    Time: 2017-09-04 23:59:59+00:00 | Close: 0.028319954872131348
    Time: 2017-09-05 23:59:59+00:00 | Close: -0.02631998062133789
    Time: 2017-09-06 23:59:59+00:00 | Close: 0.0008599758148193359
    Time: 2017-09-07 23:59:59+00:00 | Close: -0.00373995304107666
    Time: 2017-09-08 23:59:59+00:00 | Close: 0.005540013313293457
    Time: 2017-09-09 23:59:59+00:00 | Close: -0.0056400299072265625
    Time: 2017-09-10 23:59:59+00:00 | Close: 0.004199981689453125
    Time: 2017-09-11 23:59:59+00:00 | Close: -0.004379987716674805
    Time: 2017-09-12 23:59:59+00:00 | Close: 0.004220008850097656
    Time: 2017-09-13 23:59:59+00:00 | Close: -0.0027500391006469727
    Time: 2017-09-14 23:59:59+00:00 | Close: 0.0005899667739868164
    Time: 2017-09-15 23:59:59+00:00 | Close: 0.0022400617599487305
    Time: 2017-09-16 23:59:59+00:00 | Close: -0.0033800601959228516
    Time: 2017-09-17 23:59:59+00:00 | Close: 0.004580020904541016
    Time: 2017-09-18 23:59:59+00:00 | Close: -0.0041599273681640625
    Time: 2017-09-19 23:59:59+00:00 | Close: -0.0005600452423095703
    Time: 2017-09-20 23:59:59+00:00 | Close: 0.002689957618713379
    Time: 2017-09-21 23:59:59+00:00 | Close: 0.0001800060272216797
    Time: 2017-09-22 23:59:59+00:00 | Close: -0.00012993812561035156
    Time: 2017-09-23 23:59:59+00:00 | Close: -0.0025000572204589844
    Time: 2017-09-24 23:59:59+00:00 | Close: 0.0008400678634643555
    Time: 2017-09-25 23:59:59+00:00 | Close: -0.0016300678253173828
    Time: 2017-09-26 23:59:59+00:00 | Close: 0.001289963722229004
    Time: 2017-09-27 23:59:59+00:00 | Close: -0.001949906349182129
    Time: 2017-09-28 23:59:59+00:00 | Close: 0.0011500120162963867
    Time: 2017-09-29 23:59:59+00:00 | Close: -0.001927018165588379
    Time: 2017-09-30 23:59:59+00:00 | Close: -0.0033750534057617188
    Time: 2017-10-01 23:59:59+00:00 | Close: 0.0034360289573669434
    Time: 2017-10-02 23:59:59+00:00 | Close: 0.0017760396003723145
    Time: 2017-10-03 23:59:59+00:00 | Close: -0.0015799999237060547
    Time: 2017-10-04 23:59:59+00:00 | Close: 0.0011299848556518555
    Time: 2017-10-05 23:59:59+00:00 | Close: -0.0009499788284301758
    Time: 2017-10-06 23:59:59+00:00 | Close: 0.0007899999618530273
    Time: 2017-10-07 23:59:59+00:00 | Close: -0.0017700791358947754
    Time: 2017-10-08 23:59:59+00:00 | Close: -0.0008779764175415039
    Time: 2017-10-09 23:59:59+00:00 | Close: 0.0013380050659179688
    Time: 2017-10-10 23:59:59+00:00 | Close: -0.0003389716148376465
    Time: 2017-10-11 23:59:59+00:00 | Close: -0.000816047191619873
    Time: 2017-10-12 23:59:59+00:00 | Close: -0.0012019872665405273
    Time: 2017-10-13 23:59:59+00:00 | Close: 0.002626955509185791
    Time: 2017-10-14 23:59:59+00:00 | Close: -0.0003409385681152344
    Time: 2017-10-15 23:59:59+00:00 | Close: -0.00046700239181518555
    Time: 2017-10-16 23:59:59+00:00 | Close: -0.0012320280075073242
    Time: 2017-10-17 23:59:59+00:00 | Close: 0.0013250112533569336
    Time: 2017-10-18 23:59:59+00:00 | Close: 0.0033449530601501465
    Time: 2017-10-19 23:59:59+00:00 | Close: -0.0020200014114379883
    Time: 2017-10-20 23:59:59+00:00 | Close: 0.0003600120544433594
    Time: 2017-10-21 23:59:59+00:00 | Close: -9.000301361083984e-05
    Time: 2017-10-22 23:59:59+00:00 | Close: 0.001000046730041504
    Time: 2017-10-23 23:59:59+00:00 | Close: -0.00539398193359375
    Time: 2017-10-24 23:59:59+00:00 | Close: 0.006214022636413574
    Time: 2017-10-25 23:59:59+00:00 | Close: -0.0004900693893432617
    Time: 2017-10-26 23:59:59+00:00 | Close: -0.002391993999481201
    Time: 2017-10-27 23:59:59+00:00 | Close: 0.00020200014114379883
    Time: 2017-10-28 23:59:59+00:00 | Close: 0.0038900375366210938
    Time: 2017-10-29 23:59:59+00:00 | Close: -0.002850055694580078
    Time: 2017-10-30 23:59:59+00:00 | Close: -0.0005300045013427734
    Time: 2017-10-31 23:59:59+00:00 | Close: 0.00013005733489990234
    Time: 2017-11-01 23:59:59+00:00 | Close: 0.0008399486541748047
    Time: 2017-11-02 23:59:59+00:00 | Close: -0.0005499124526977539
    Time: 2017-11-03 23:59:59+00:00 | Close: 0.005319952964782715
    Time: 2017-11-04 23:59:59+00:00 | Close: -0.004230022430419922
    Time: 2017-11-05 23:59:59+00:00 | Close: -0.0032899975776672363
    Time: 2017-11-06 23:59:59+00:00 | Close: 0.00457996129989624
    Time: 2017-11-07 23:59:59+00:00 | Close: 0.002280116081237793
    Time: 2017-11-08 23:59:59+00:00 | Close: 0.0062999725341796875
    Time: 2017-11-09 23:59:59+00:00 | Close: -0.0037800073623657227
    Time: 2017-11-10 23:59:59+00:00 | Close: -0.002169966697692871
    Time: 2017-11-11 23:59:59+00:00 | Close: 0.0029799938201904297
    Time: 2017-11-12 23:59:59+00:00 | Close: 0.0034799575805664062
    Time: 2017-11-13 23:59:59+00:00 | Close: -0.0031200647354125977
    Time: 2017-11-14 23:59:59+00:00 | Close: -0.002519965171813965
    Time: 2017-11-15 23:59:59+00:00 | Close: -0.0036499500274658203
    Time: 2017-11-16 23:59:59+00:00 | Close: -0.0010600090026855469
    Time: 2017-11-17 23:59:59+00:00 | Close: -0.0007300376892089844
    Time: 2017-11-18 23:59:59+00:00 | Close: 0.0009200572967529297
    Time: 2017-11-19 23:59:59+00:00 | Close: 0.00012993812561035156
    Time: 2017-11-20 23:59:59+00:00 | Close: -0.0005199909210205078
    Time: 2017-11-21 23:59:59+00:00 | Close: -0.005872964859008789
    Time: 2017-11-22 23:59:59+00:00 | Close: 0.004102945327758789
    Time: 2017-11-23 23:59:59+00:00 | Close: -0.005518972873687744
    Time: 2017-11-24 23:59:59+00:00 | Close: 0.007698953151702881
    Time: 2017-11-25 23:59:59+00:00 | Close: 0.003080010414123535
    Time: 2017-11-26 23:59:59+00:00 | Close: 0.0032700300216674805
    Time: 2017-11-27 23:59:59+00:00 | Close: -0.007390022277832031
    Time: 2017-11-28 23:59:59+00:00 | Close: -0.0011500120162963867
    Time: 2017-11-29 23:59:59+00:00 | Close: -0.009533941745758057
    Time: 2017-11-30 23:59:59+00:00 | Close: 0.017494022846221924
    Time: 2017-12-01 23:59:59+00:00 | Close: 0.0016800165176391602
    Time: 2017-12-02 23:59:59+00:00 | Close: -0.010126054286956787
    Time: 2017-12-03 23:59:59+00:00 | Close: 0.0010059475898742676
    Time: 2017-12-04 23:59:59+00:00 | Close: 0.0030100345611572266
    Time: 2017-12-05 23:59:59+00:00 | Close: -0.0016999244689941406
    Time: 2017-12-06 23:59:59+00:00 | Close: 0.007939934730529785
    Time: 2017-12-07 23:59:59+00:00 | Close: 0.02174997329711914
    Time: 2017-12-08 23:59:59+00:00 | Close: -0.014059901237487793
    Time: 2017-12-09 23:59:59+00:00 | Close: -0.00047004222869873047
    Time: 2017-12-10 23:59:59+00:00 | Close: 0.0006200075149536133
    Time: 2017-12-11 23:59:59+00:00 | Close: 0.0008100271224975586
    Time: 2017-12-12 23:59:59+00:00 | Close: 0.05931997299194336
    Time: 2017-12-13 23:59:59+00:00 | Close: -0.0507199764251709
    Time: 2017-12-14 23:59:59+00:00 | Close: -0.018970012664794922
    Time: 2017-12-15 23:59:59+00:00 | Close: 0.007910013198852539
    Time: 2017-12-16 23:59:59+00:00 | Close: -0.008680105209350586
    Time: 2017-12-17 23:59:59+00:00 | Close: 0.0018200874328613281
    Time: 2017-12-18 23:59:59+00:00 | Close: 0.0037800073623657227
    Time: 2017-12-19 23:59:59+00:00 | Close: -0.002340078353881836
    Time: 2017-12-20 23:59:59+00:00 | Close: -0.010499954223632812
    Time: 2017-12-21 23:59:59+00:00 | Close: 0.009029984474182129
    Time: 2017-12-22 23:59:59+00:00 | Close: 0.008740067481994629
    Time: 2017-12-23 23:59:59+00:00 | Close: 0.027309894561767578
    Time: 2017-12-24 23:59:59+00:00 | Close: -0.022229909896850586
    Time: 2017-12-25 23:59:59+00:00 | Close: -0.011900067329406738
    Time: 2017-12-26 23:59:59+00:00 | Close: -0.007059931755065918
    Time: 2017-12-27 23:59:59+00:00 | Close: -0.0004100799560546875
    Time: 2017-12-28 23:59:59+00:00 | Close: 0.0029300451278686523
    Time: 2017-12-29 23:59:59+00:00 | Close: -0.0009499788284301758
    Time: 2017-12-30 23:59:59+00:00 | Close: 0.015709996223449707
    Time: 2017-12-31 23:59:59+00:00 | Close: -0.009090065956115723
    Time: 2018-01-01 23:59:59+00:00 | Close: -0.004979968070983887
    Time: 2018-01-02 23:59:59+00:00 | Close: -0.0023800134658813477
    Time: 2018-01-03 23:59:59+00:00 | Close: 0.008540034294128418
    Time: 2018-01-04 23:59:59+00:00 | Close: -0.0109100341796875
    Time: 2018-01-05 23:59:59+00:00 | Close: -0.003895998001098633
    Time: 2018-01-06 23:59:59+00:00 | Close: 0.01035606861114502
    Time: 2018-01-07 23:59:59+00:00 | Close: -0.007420063018798828
    Time: 2018-01-08 23:59:59+00:00 | Close: 0.007750034332275391
    Time: 2018-01-09 23:59:59+00:00 | Close: -0.0033299922943115234
    Time: 2018-01-10 23:59:59+00:00 | Close: -0.004710078239440918
    Time: 2018-01-11 23:59:59+00:00 | Close: 0.00043010711669921875
    Time: 2018-01-12 23:59:59+00:00 | Close: 0.004369974136352539
    Time: 2018-01-13 23:59:59+00:00 | Close: -0.004060029983520508
    Time: 2018-01-14 23:59:59+00:00 | Close: 0.014099955558776855
    Time: 2018-01-15 23:59:59+00:00 | Close: -0.009499907493591309
    Time: 2018-01-16 23:59:59+00:00 | Close: 0.02752995491027832
    Time: 2018-01-17 23:59:59+00:00 | Close: -0.019620060920715332
    Time: 2018-01-18 23:59:59+00:00 | Close: 0.00858008861541748
    Time: 2018-01-19 23:59:59+00:00 | Close: -0.01857006549835205
    Time: 2018-01-20 23:59:59+00:00 | Close: -0.003430008888244629
    Time: 2018-01-21 23:59:59+00:00 | Close: -0.0012489557266235352
    Time: 2018-01-22 23:59:59+00:00 | Close: 0.005179047584533691
    Time: 2018-01-23 23:59:59+00:00 | Close: 9.894371032714844e-06
    Time: 2018-01-24 23:59:59+00:00 | Close: -0.007565915584564209
    Time: 2018-01-25 23:59:59+00:00 | Close: 0.0021109580993652344
    Time: 2018-01-26 23:59:59+00:00 | Close: 0.004545032978057861
    Time: 2018-01-27 23:59:59+00:00 | Close: -0.010815024375915527
    Time: 2018-01-28 23:59:59+00:00 | Close: -0.004535019397735596
    Time: 2018-01-29 23:59:59+00:00 | Close: 0.006529033184051514
    Time: 2018-01-30 23:59:59+00:00 | Close: -0.008832991123199463
    Time: 2018-01-31 23:59:59+00:00 | Close: 0.003787994384765625
    Time: 2018-02-01 23:59:59+00:00 | Close: -0.0033349990844726562
    Time: 2018-02-02 23:59:59+00:00 | Close: 0.003807961940765381
    Time: 2018-02-03 23:59:59+00:00 | Close: 0.010563015937805176
    Time: 2018-02-04 23:59:59+00:00 | Close: 0.008820056915283203
    Time: 2018-02-05 23:59:59+00:00 | Close: -0.013822019100189209
    Time: 2018-02-06 23:59:59+00:00 | Close: 0.013781964778900146
    Time: 2018-02-07 23:59:59+00:00 | Close: -0.0086899995803833
    Time: 2018-02-08 23:59:59+00:00 | Close: 0.017510056495666504
    Time: 2018-02-09 23:59:59+00:00 | Close: -0.01680004596710205
    Time: 2018-02-10 23:59:59+00:00 | Close: 0.0015900135040283203
    Time: 2018-02-11 23:59:59+00:00 | Close: -0.004449009895324707
    Time: 2018-02-12 23:59:59+00:00 | Close: 0.0008389949798583984
    Time: 2018-02-13 23:59:59+00:00 | Close: 0.0010099411010742188
    Time: 2018-02-14 23:59:59+00:00 | Close: -0.0003299713134765625
    Time: 2018-02-15 23:59:59+00:00 | Close: 0.004639983177185059
    Time: 2018-02-16 23:59:59+00:00 | Close: -0.003309965133666992
    Time: 2018-02-17 23:59:59+00:00 | Close: 0.001600027084350586
    Time: 2018-02-18 23:59:59+00:00 | Close: 0.0014899969100952148
    Time: 2018-02-19 23:59:59+00:00 | Close: -0.004580020904541016
    Time: 2018-02-20 23:59:59+00:00 | Close: 0.0
    Time: 2018-02-21 23:59:59+00:00 | Close: 0.0003600120544433594
    Time: 2018-02-22 23:59:59+00:00 | Close: 0.003119945526123047
    Time: 2018-02-23 23:59:59+00:00 | Close: -0.002519965171813965
    Time: 2018-02-24 23:59:59+00:00 | Close: 0.0012700557708740234
    Time: 2018-02-25 23:59:59+00:00 | Close: -0.0025000572204589844
    Time: 2018-02-26 23:59:59+00:00 | Close: -0.0007789731025695801
    Time: 2018-02-27 23:59:59+00:00 | Close: 0.0009589791297912598
    Time: 2018-02-28 23:59:59+00:00 | Close: -0.0016170144081115723
    Time: 2018-03-01 23:59:59+00:00 | Close: 0.0015169978141784668
    Time: 2018-03-02 23:59:59+00:00 | Close: -0.0006899833679199219
    Time: 2018-03-03 23:59:59+00:00 | Close: 0.001139998435974121
    Time: 2018-03-04 23:59:59+00:00 | Close: -0.0032579898834228516
    Time: 2018-03-05 23:59:59+00:00 | Close: 0.00125199556350708
    Time: 2018-03-06 23:59:59+00:00 | Close: 0.0016359686851501465
    Time: 2018-03-07 23:59:59+00:00 | Close: 0.0019800662994384766
    Time: 2018-03-08 23:59:59+00:00 | Close: 0.003430008888244629
    Time: 2018-03-09 23:59:59+00:00 | Close: -0.004250049591064453
    Time: 2018-03-10 23:59:59+00:00 | Close: 0.0035300254821777344
    Time: 2018-03-11 23:59:59+00:00 | Close: -0.0013500452041625977
    Time: 2018-03-12 23:59:59+00:00 | Close: -0.0014899969100952148
    Time: 2018-03-13 23:59:59+00:00 | Close: -0.0025069713592529297
    Time: 2018-03-14 23:59:59+00:00 | Close: 0.0029070377349853516
    Time: 2018-03-15 23:59:59+00:00 | Close: -0.0014700889587402344
    Time: 2018-03-16 23:59:59+00:00 | Close: -0.0027289390563964844
    Time: 2018-03-17 23:59:59+00:00 | Close: 0.0030690431594848633
    Time: 2018-03-18 23:59:59+00:00 | Close: 0.001459956169128418
    Time: 2018-03-19 23:59:59+00:00 | Close: -0.013213038444519043
    Time: 2018-03-20 23:59:59+00:00 | Close: 0.006965041160583496
    Time: 2018-03-21 23:59:59+00:00 | Close: 0.002411961555480957
    Time: 2018-03-22 23:59:59+00:00 | Close: -0.0002619624137878418
    Time: 2018-03-23 23:59:59+00:00 | Close: -0.00874704122543335
    Time: 2018-03-24 23:59:59+00:00 | Close: 0.018864989280700684
    Time: 2018-03-25 23:59:59+00:00 | Close: -0.009413957595825195
    Time: 2018-03-26 23:59:59+00:00 | Close: 0.0037239789962768555
    Time: 2018-03-27 23:59:59+00:00 | Close: -0.001799941062927246
    Time: 2018-03-28 23:59:59+00:00 | Close: -0.0024060606956481934
    Time: 2018-03-29 23:59:59+00:00 | Close: -0.0005809664726257324
    Time: 2018-03-30 23:59:59+00:00 | Close: 0.0003199577331542969
    Time: 2018-03-31 23:59:59+00:00 | Close: 0.0018270015716552734
    Time: 2018-04-01 23:59:59+00:00 | Close: -0.0009599924087524414
    Time: 2018-04-02 23:59:59+00:00 | Close: 0.00032007694244384766
    Time: 2018-04-03 23:59:59+00:00 | Close: 0.00023996829986572266
    Time: 2018-04-04 23:59:59+00:00 | Close: 0.00046002864837646484
    Time: 2018-04-05 23:59:59+00:00 | Close: 0.0016999244689941406
    Time: 2018-04-06 23:59:59+00:00 | Close: -0.0014399290084838867
    Time: 2018-04-07 23:59:59+00:00 | Close: -0.001446068286895752
    Time: 2018-04-08 23:59:59+00:00 | Close: -0.0028349757194519043
    Time: 2018-04-09 23:59:59+00:00 | Close: 0.0007460117340087891
    Time: 2018-04-10 23:59:59+00:00 | Close: -0.0001990199089050293
    Time: 2018-04-11 23:59:59+00:00 | Close: 0.002893984317779541
    Time: 2018-04-12 23:59:59+00:00 | Close: -0.0034189820289611816
    Time: 2018-04-13 23:59:59+00:00 | Close: 0.0020639896392822266
    Time: 2018-04-14 23:59:59+00:00 | Close: 0.0008710026741027832
    Time: 2018-04-15 23:59:59+00:00 | Close: -0.0011640191078186035
    Time: 2018-04-16 23:59:59+00:00 | Close: -0.0010100007057189941
    Time: 2018-04-17 23:59:59+00:00 | Close: 0.000964045524597168
    Time: 2018-04-18 23:59:59+00:00 | Close: -0.0009469985961914062
    Time: 2018-04-19 23:59:59+00:00 | Close: -0.0004240274429321289
    Time: 2018-04-20 23:59:59+00:00 | Close: 0.0011529922485351562
    Time: 2018-04-21 23:59:59+00:00 | Close: 0.0006760358810424805
    Time: 2018-04-22 23:59:59+00:00 | Close: -0.0028180480003356934
    Time: 2018-04-23 23:59:59+00:00 | Close: 0.0016510486602783203
    Time: 2018-04-24 23:59:59+00:00 | Close: 0.00691300630569458
    Time: 2018-04-25 23:59:59+00:00 | Close: -0.012951016426086426
    Time: 2018-04-26 23:59:59+00:00 | Close: 0.007804989814758301
    Time: 2018-04-27 23:59:59+00:00 | Close: 0.004536032676696777
    Time: 2018-04-28 23:59:59+00:00 | Close: -0.004815042018890381
    Time: 2018-04-29 23:59:59+00:00 | Close: -0.0013189911842346191
    Time: 2018-04-30 23:59:59+00:00 | Close: 0.000903010368347168
    Time: 2018-05-01 23:59:59+00:00 | Close: 0.004570960998535156
    Time: 2018-05-02 23:59:59+00:00 | Close: -0.006025969982147217
    Time: 2018-05-03 23:59:59+00:00 | Close: 0.0005090236663818359
    Time: 2018-05-04 23:59:59+00:00 | Close: 0.0005879998207092285
    Time: 2018-05-05 23:59:59+00:00 | Close: -0.0022770166397094727
    Time: 2018-05-06 23:59:59+00:00 | Close: 0.000917971134185791
    Time: 2018-05-07 23:59:59+00:00 | Close: 3.504753112792969e-05
    Time: 2018-05-08 23:59:59+00:00 | Close: 0.004882991313934326
    Time: 2018-05-09 23:59:59+00:00 | Close: -0.0016100406646728516
    Time: 2018-05-10 23:59:59+00:00 | Close: 0.0008300542831420898
    Time: 2018-05-11 23:59:59+00:00 | Close: 0.0009099245071411133
    Time: 2018-05-12 23:59:59+00:00 | Close: -0.0011500120162963867
    Time: 2018-05-13 23:59:59+00:00 | Close: 0.0021500587463378906
    Time: 2018-05-14 23:59:59+00:00 | Close: -0.0019799470901489258
    Time: 2018-05-15 23:59:59+00:00 | Close: -0.00013005733489990234
    Time: 2018-05-16 23:59:59+00:00 | Close: -0.0011900067329406738
    Time: 2018-05-17 23:59:59+00:00 | Close: 0.00024002790451049805
    Time: 2018-05-18 23:59:59+00:00 | Close: 0.0009199380874633789
    Time: 2018-05-19 23:59:59+00:00 | Close: -0.0007499456405639648
    Time: 2018-05-20 23:59:59+00:00 | Close: -0.001242995262145996
    Time: 2018-05-21 23:59:59+00:00 | Close: 0.0038529634475708008
    Time: 2018-05-22 23:59:59+00:00 | Close: 0.0
    Time: 2018-05-23 23:59:59+00:00 | Close: 0.0010499954223632812
    Time: 2018-05-24 23:59:59+00:00 | Close: -0.005201995372772217
    Time: 2018-05-25 23:59:59+00:00 | Close: 0.001622021198272705
    Time: 2018-05-26 23:59:59+00:00 | Close: -0.0005499720573425293
    Time: 2018-05-27 23:59:59+00:00 | Close: -0.0007080435752868652
    Time: 2018-05-28 23:59:59+00:00 | Close: 0.0033080577850341797
    Time: 2018-05-29 23:59:59+00:00 | Close: -0.0018100738525390625
    Time: 2018-05-30 23:59:59+00:00 | Close: -0.0009529590606689453
    Time: 2018-05-31 23:59:59+00:00 | Close: -0.0017240047454833984
    Time: 2018-06-01 23:59:59+00:00 | Close: 0.0029870271682739258
    Time: 2018-06-02 23:59:59+00:00 | Close: -0.007460057735443115
    Time: 2018-06-03 23:59:59+00:00 | Close: 0.006570041179656982
    Time: 2018-06-04 23:59:59+00:00 | Close: 0.00041997432708740234
    Time: 2018-06-05 23:59:59+00:00 | Close: 0.0004999637603759766
    Time: 2018-06-06 23:59:59+00:00 | Close: -0.0003299713134765625
    Time: 2018-06-07 23:59:59+00:00 | Close: -0.001940011978149414
    Time: 2018-06-08 23:59:59+00:00 | Close: 0.0030400753021240234
    Time: 2018-06-09 23:59:59+00:00 | Close: 0.004289984703063965
    Time: 2018-06-10 23:59:59+00:00 | Close: -0.00786501169204712
    Time: 2018-06-11 23:59:59+00:00 | Close: 0.0037149786949157715
    Time: 2018-06-12 23:59:59+00:00 | Close: -0.0011600255966186523
    Time: 2018-06-13 23:59:59+00:00 | Close: 0.0027600526809692383
    Time: 2018-06-14 23:59:59+00:00 | Close: 0.00041997432708740234
    Time: 2018-06-15 23:59:59+00:00 | Close: 0.003000020980834961
    Time: 2018-06-16 23:59:59+00:00 | Close: -0.00270998477935791
    Time: 2018-06-17 23:59:59+00:00 | Close: 0.0012400150299072266
    Time: 2018-06-18 23:59:59+00:00 | Close: -0.002650022506713867
    Time: 2018-06-19 23:59:59+00:00 | Close: -0.0026100873947143555
    Time: 2018-06-20 23:59:59+00:00 | Close: -0.0013909339904785156
    Time: 2018-06-21 23:59:59+00:00 | Close: 0.0017009973526000977
    Time: 2018-06-22 23:59:59+00:00 | Close: 0.0024700164794921875
    Time: 2018-06-23 23:59:59+00:00 | Close: -0.0010200738906860352
    Time: 2018-06-24 23:59:59+00:00 | Close: 0.0031200647354125977
    Time: 2018-06-25 23:59:59+00:00 | Close: -0.00448000431060791
    Time: 2018-06-26 23:59:59+00:00 | Close: -5.996227264404297e-05
    Time: 2018-06-27 23:59:59+00:00 | Close: -0.0026250481605529785
    Time: 2018-06-28 23:59:59+00:00 | Close: -0.0007420182228088379
    Time: 2018-06-29 23:59:59+00:00 | Close: 0.0061370134353637695
    Time: 2018-06-30 23:59:59+00:00 | Close: -0.004137992858886719
    Time: 2018-07-01 23:59:59+00:00 | Close: -0.00037097930908203125
    Time: 2018-07-02 23:59:59+00:00 | Close: 3.796815872192383e-05
    Time: 2018-07-03 23:59:59+00:00 | Close: 0.0014609694480895996
    Time: 2018-07-04 23:59:59+00:00 | Close: -0.0011249780654907227
    Time: 2018-07-05 23:59:59+00:00 | Close: 0.006945013999938965
    Time: 2018-07-06 23:59:59+00:00 | Close: -0.0029799938201904297
    Time: 2018-07-07 23:59:59+00:00 | Close: 0.0030499696731567383
    Time: 2018-07-08 23:59:59+00:00 | Close: -0.0019599199295043945
    Time: 2018-07-09 23:59:59+00:00 | Close: 0.0032500028610229492
    Time: 2018-07-10 23:59:59+00:00 | Close: -0.006300091743469238
    Time: 2018-07-11 23:59:59+00:00 | Close: -3.993511199951172e-05
    Time: 2018-07-12 23:59:59+00:00 | Close: -0.0020900368690490723
    Time: 2018-07-13 23:59:59+00:00 | Close: 0.002350032329559326
    Time: 2018-07-14 23:59:59+00:00 | Close: 0.001230001449584961
    Time: 2018-07-15 23:59:59+00:00 | Close: -0.004298031330108643
    Time: 2018-07-16 23:59:59+00:00 | Close: 0.0007870197296142578
    Time: 2018-07-17 23:59:59+00:00 | Close: 0.00099104642868042
    Time: 2018-07-18 23:59:59+00:00 | Close: 0.0020799636840820312
    Time: 2018-07-19 23:59:59+00:00 | Close: -0.004122018814086914
    Time: 2018-07-20 23:59:59+00:00 | Close: 0.0029419660568237305
    Time: 2018-07-21 23:59:59+00:00 | Close: -0.0009899139404296875
    Time: 2018-07-22 23:59:59+00:00 | Close: -0.0001970529556274414
    Time: 2018-07-23 23:59:59+00:00 | Close: -0.0023469924926757812
    Time: 2018-07-24 23:59:59+00:00 | Close: -0.0009909868240356445
    Time: 2018-07-25 23:59:59+00:00 | Close: 0.0022859573364257812
    Time: 2018-07-26 23:59:59+00:00 | Close: -0.0008400082588195801
    Time: 2018-07-27 23:59:59+00:00 | Close: -0.000832974910736084
    Time: 2018-07-28 23:59:59+00:00 | Close: 0.0007690191268920898
    Time: 2018-07-29 23:59:59+00:00 | Close: 0.0010319948196411133
    Time: 2018-07-30 23:59:59+00:00 | Close: -9.01016235355101e-06
    Time: 2018-07-31 23:59:59+00:00 | Close: 0.0005970000000000697
    Time: 2018-08-01 23:59:59+00:00 | Close: -9.80000000000425e-05
    Time: 2018-08-02 23:59:59+00:00 | Close: 0.0012510000000001131
    Time: 2018-08-03 23:59:59+00:00 | Close: -0.0015650000000001496
    Time: 2018-08-04 23:59:59+00:00 | Close: -0.0005899999999999794
    Time: 2018-08-05 23:59:59+00:00 | Close: 0.0008420000000000094
    Time: 2018-08-06 23:59:59+00:00 | Close: 0.001603000000000021
    Time: 2018-08-07 23:59:59+00:00 | Close: 0.0005900000000000905
    Time: 2018-08-08 23:59:59+00:00 | Close: 0.00014999999999987246
    Time: 2018-08-09 23:59:59+00:00 | Close: 0.0025500000000000522
    Time: 2018-08-10 23:59:59+00:00 | Close: -0.0026600000000001067
    Time: 2018-08-11 23:59:59+00:00 | Close: 0.00827
    Time: 2018-08-12 23:59:59+00:00 | Close: -0.009359999999999813
    Time: 2018-08-13 23:59:59+00:00 | Close: 0.0034399999999998876
    Time: 2018-08-14 23:59:59+00:00 | Close: -0.0063870000000000315
    Time: 2018-08-15 23:59:59+00:00 | Close: 0.003707000000000016
    Time: 2018-08-16 23:59:59+00:00 | Close: -2.999999999997449e-05
    Time: 2018-08-17 23:59:59+00:00 | Close: -0.00345899999999999
    Time: 2018-08-18 23:59:59+00:00 | Close: 0.005099000000000076
    Time: 2018-08-19 23:59:59+00:00 | Close: -0.0023400000000000087
    Time: 2018-08-20 23:59:59+00:00 | Close: 0.00486999999999993
    Time: 2018-08-21 23:59:59+00:00 | Close: -0.004690000000000083
    Time: 2018-08-22 23:59:59+00:00 | Close: -0.00034999999999985043
    Time: 2018-08-23 23:59:59+00:00 | Close: -0.0013740000000000974
    Time: 2018-08-24 23:59:59+00:00 | Close: 0.0028039999999999177
    Time: 2018-08-25 23:59:59+00:00 | Close: -0.0007800000000000029
    Time: 2018-08-26 23:59:59+00:00 | Close: -0.0017729999999999135
    Time: 2018-08-27 23:59:59+00:00 | Close: -0.0014250000000000096
    Time: 2018-08-28 23:59:59+00:00 | Close: 0.0015930000000000666
    Time: 2018-08-29 23:59:59+00:00 | Close: 0.0012650000000000716
    Time: 2018-08-30 23:59:59+00:00 | Close: -0.0006300000000001305
    Time: 2018-08-31 23:59:59+00:00 | Close: 0.0034799999999999276
    Time: 2018-09-01 23:59:59+00:00 | Close: -0.006696999999999953
    Time: 2018-09-02 23:59:59+00:00 | Close: 0.0010260000000000824
    Time: 2018-09-03 23:59:59+00:00 | Close: 0.0008029999999999982
    Time: 2018-09-04 23:59:59+00:00 | Close: 0.0008749999999999591
    Time: 2018-09-05 23:59:59+00:00 | Close: 0.008432999999999913
    Time: 2018-09-06 23:59:59+00:00 | Close: -0.007039999999999935
    Time: 2018-09-07 23:59:59+00:00 | Close: 0.005449999999999955
    Time: 2018-09-08 23:59:59+00:00 | Close: -0.0020799999999998597
    Time: 2018-09-09 23:59:59+00:00 | Close: 0.0006999999999999229
    Time: 2018-09-10 23:59:59+00:00 | Close: -0.0037000000000000366
    Time: 2018-09-11 23:59:59+00:00 | Close: 0.0032600000000000406
    Time: 2018-09-12 23:59:59+00:00 | Close: -0.003290000000000015
    Time: 2018-09-13 23:59:59+00:00 | Close: 0.0051000000000001044
    Time: 2018-09-14 23:59:59+00:00 | Close: -0.00399000000000016
    Time: 2018-09-15 23:59:59+00:00 | Close: -0.0014999999999998348
    Time: 2018-09-16 23:59:59+00:00 | Close: 9.999999999998899e-05
    Time: 2018-09-17 23:59:59+00:00 | Close: 0.003149999999999986
    Time: 2018-09-18 23:59:59+00:00 | Close: -0.0018599999999999728
    Time: 2018-09-19 23:59:59+00:00 | Close: -0.0015600000000000058
    Time: 2018-09-20 23:59:59+00:00 | Close: 0.0008500000000000174
    Time: 2018-09-21 23:59:59+00:00 | Close: -0.007112000000000118
    Time: 2018-09-22 23:59:59+00:00 | Close: 0.006492000000000053
    Time: 2018-09-23 23:59:59+00:00 | Close: -0.0014080000000000759
    Time: 2018-09-24 23:59:59+00:00 | Close: 0.0011179999999999524
    Time: 2018-09-25 23:59:59+00:00 | Close: -0.00018999999999991246
    Time: 2018-09-26 23:59:59+00:00 | Close: 0.0016899999999999693
    Time: 2018-09-27 23:59:59+00:00 | Close: -0.005023
    Time: 2018-09-28 23:59:59+00:00 | Close: 0.004313000000000011
    Time: 2018-09-29 23:59:59+00:00 | Close: -0.0018179999999999863
    Time: 2018-09-30 23:59:59+00:00 | Close: 0.0007579999999999254
    Time: 2018-10-01 23:59:59+00:00 | Close: -0.002434999999999965
    Time: 2018-10-02 23:59:59+00:00 | Close: 0.0018160000000000398
    Time: 2018-10-03 23:59:59+00:00 | Close: -0.0011719999999999509
    Time: 2018-10-04 23:59:59+00:00 | Close: -0.0023840000000000527
    Time: 2018-10-05 23:59:59+00:00 | Close: -0.0004069999999999352
    Time: 2018-10-06 23:59:59+00:00 | Close: 0.001398999999999928
    Time: 2018-10-07 23:59:59+00:00 | Close: -0.0005600000000000049
    Time: 2018-10-08 23:59:59+00:00 | Close: -0.0008029999999999982
    Time: 2018-10-09 23:59:59+00:00 | Close: 0.0009649999999999936
    Time: 2018-10-10 23:59:59+00:00 | Close: -0.0032769999999999744
    Time: 2018-10-11 23:59:59+00:00 | Close: -0.00047600000000003195
    Time: 2018-10-12 23:59:59+00:00 | Close: 0.001076000000000077
    Time: 2018-10-13 23:59:59+00:00 | Close: -0.006056000000000061
    Time: 2018-10-14 23:59:59+00:00 | Close: 0.0015239999999999698
    Time: 2018-10-15 23:59:59+00:00 | Close: -0.009431999999999996
    Time: 2018-10-16 23:59:59+00:00 | Close: -0.004985999999999935
    Time: 2018-10-17 23:59:59+00:00 | Close: -0.003927000000000014
    Time: 2018-10-18 23:59:59+00:00 | Close: 0.009633000000000003
    Time: 2018-10-19 23:59:59+00:00 | Close: 0.006854000000000027
    Time: 2018-10-20 23:59:59+00:00 | Close: -0.0038810000000000233
    Time: 2018-10-21 23:59:59+00:00 | Close: -0.0002830000000000332
    Time: 2018-10-22 23:59:59+00:00 | Close: 0.00045000000000006146
    Time: 2018-10-23 23:59:59+00:00 | Close: 0.0039639999999999675
    Time: 2018-10-24 23:59:59+00:00 | Close: 0.0006500000000000394
    Time: 2018-10-25 23:59:59+00:00 | Close: 0.00017899999999992922
    Time: 2018-10-26 23:59:59+00:00 | Close: 0.0009980000000000544
    Time: 2018-10-27 23:59:59+00:00 | Close: 0.0033079999999999776
    Time: 2018-10-28 23:59:59+00:00 | Close: 0.005356000000000027
    Time: 2018-10-29 23:59:59+00:00 | Close: -0.0015939999999999843
    Time: 2018-10-30 23:59:59+00:00 | Close: -0.000188000000000077
    Time: 2018-10-31 23:59:59+00:00 | Close: -0.008549000000000029
    Time: 2018-11-01 23:59:59+00:00 | Close: 0.003598000000000101
    Time: 2018-11-02 23:59:59+00:00 | Close: 0.0017809999999999215
    Time: 2018-11-03 23:59:59+00:00 | Close: 0.005932000000000048
    Time: 2018-11-04 23:59:59+00:00 | Close: -0.010724999999999985
    Time: 2018-11-05 23:59:59+00:00 | Close: 0.0044679999999999165
    Time: 2018-11-06 23:59:59+00:00 | Close: -0.00037999999999993594
    Time: 2018-11-07 23:59:59+00:00 | Close: 0.00047399999999997444
    Time: 2018-11-08 23:59:59+00:00 | Close: 0.0010630000000000361
    Time: 2018-11-09 23:59:59+00:00 | Close: 0.0004990000000000272
    Time: 2018-11-10 23:59:59+00:00 | Close: 0.0023479999999999057
    Time: 2018-11-11 23:59:59+00:00 | Close: -0.006718000000000002
    Time: 2018-11-12 23:59:59+00:00 | Close: -0.0013139999999999263
    Time: 2018-11-13 23:59:59+00:00 | Close: -0.004029999999999978
    Time: 2018-11-14 23:59:59+00:00 | Close: -0.0184740000000001
    Time: 2018-11-15 23:59:59+00:00 | Close: 0.015378000000000003
    Time: 2018-11-16 23:59:59+00:00 | Close: 0.005005000000000037
    Time: 2018-11-17 23:59:59+00:00 | Close: -0.0011579999999999924
    Time: 2018-11-18 23:59:59+00:00 | Close: 0.006664000000000003
    Time: 2018-11-19 23:59:59+00:00 | Close: -0.009803000000000006
    Time: 2018-11-20 23:59:59+00:00 | Close: -0.013931000000000027
    Time: 2018-11-21 23:59:59+00:00 | Close: 0.018705000000000083
    Time: 2018-11-22 23:59:59+00:00 | Close: 0.010683999999999916
    Time: 2018-11-23 23:59:59+00:00 | Close: -0.01561799999999991
    Time: 2018-11-24 23:59:59+00:00 | Close: -0.0023460000000000703
    Time: 2018-11-25 23:59:59+00:00 | Close: 0.0007449999999999957
    Time: 2018-11-26 23:59:59+00:00 | Close: -0.003726000000000007
    Time: 2018-11-27 23:59:59+00:00 | Close: 0.007017000000000051
    Time: 2018-11-28 23:59:59+00:00 | Close: 0.014361999999999986
    Time: 2018-11-29 23:59:59+00:00 | Close: -0.0012448991890000594
    Time: 2018-11-30 23:59:59+00:00 | Close: -0.0055545088779999086
    Time: 2018-12-01 23:59:59+00:00 | Close: 0.009229690836999871
    Time: 2018-12-02 23:59:59+00:00 | Close: -0.002680619380999949
    Time: 2018-12-03 23:59:59+00:00 | Close: -0.0017778504539999185
    Time: 2018-12-04 23:59:59+00:00 | Close: 0.003437188634999977
    Time: 2018-12-05 23:59:59+00:00 | Close: -0.007065158138000016
    Time: 2018-12-06 23:59:59+00:00 | Close: 0.005330177345999942
    Time: 2018-12-07 23:59:59+00:00 | Close: 0.00313519609199997
    Time: 2018-12-08 23:59:59+00:00 | Close: 0.018544233730000137
    Time: 2018-12-09 23:59:59+00:00 | Close: -0.0044733248799999625
    Time: 2018-12-10 23:59:59+00:00 | Close: 0.0011021636999999362
    Time: 2018-12-11 23:59:59+00:00 | Close: -0.006810273809999989
    Time: 2018-12-12 23:59:59+00:00 | Close: -3.7882019999990746e-05
    Time: 2018-12-13 23:59:59+00:00 | Close: -0.006378280420000104
    Time: 2018-12-14 23:59:59+00:00 | Close: -0.0011806341100000228
    Time: 2018-12-15 23:59:59+00:00 | Close: 0.002792215659999986
    Time: 2018-12-16 23:59:59+00:00 | Close: 0.0013466939700002012
    Time: 2018-12-17 23:59:59+00:00 | Close: 0.0036047227999997933
    Time: 2018-12-18 23:59:59+00:00 | Close: 0.0029270513800001563
    Time: 2018-12-19 23:59:59+00:00 | Close: 0.009494399769999884
    Time: 2018-12-20 23:59:59+00:00 | Close: -0.0029450981499998807
    Time: 2018-12-21 23:59:59+00:00 | Close: -0.003910825860000022
    Time: 2018-12-22 23:59:59+00:00 | Close: 0.005299361939999914
    Time: 2018-12-23 23:59:59+00:00 | Close: -0.004850789759999863
    Time: 2018-12-24 23:59:59+00:00 | Close: -0.00017818645000011735
    Time: 2018-12-25 23:59:59+00:00 | Close: 0.0032731146500000197
    Time: 2018-12-26 23:59:59+00:00 | Close: 0.0004998131900000313
    Time: 2018-12-27 23:59:59+00:00 | Close: 0.0046242147999999705
    Time: 2018-12-28 23:59:59+00:00 | Close: -0.0010134630800000544
    Time: 2018-12-29 23:59:59+00:00 | Close: 0.00831216422000014
    Time: 2018-12-30 23:59:59+00:00 | Close: -0.012386737609999976
    --- Conexión Cerrada ---


![imagen.png](186822c6-6695-41d2-925e-741803afc292.png)

### **Tarea 3.2: Comparación de precios de cierre (Join)**

El objetivo es unir los precios de dos activos en una misma tabla para su comparación.
1. Crea dos pipelines separadas para los precios de cierre (``close``):
- ``btc_data`` para **``BTC``**.
- ``eth_data`` para **``ETH``**.
- Ambas deben usar el mismo rango de tiempo (ej. **año 2020**).
2. Usa la función **``join()``** para combinar ambas tablas por la marca de tiempo (``on: ["_time"]``).
3. Usa la función **``map()``** para calcular una nueva columna llamada **``ratio``** que sea el resultado de dividir el precio de BTC entre el precio de ETH (``r.btc_data._value / r.eth_data._value``).


```python
import influxdb_client
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError

INFLUX_URL = "http://influxdb-influxdb2-1:8086"
INFLUX_TOKEN = "MyInitialAdminToken0="
ORG = "docs"

print("--- Iniciando conexión a InfluxDB ---")

client = None

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=ORG
    )

    print(f"Verificando estado de salud de InfluxDB en {INFLUX_URL}")
    health = client.health()

    if health.status == "pass":
        print("[INFO] ¡Conexión Exitosa!")
        print(f"[INFO] Versión del servidor: {health.version}")

   
        ejer = """
btc_data =
  from(bucket: "crypto_raw")
    |> range(start: 2020-01-01T00:00:00Z, stop: 2020-12-31T23:59:59Z)
    |> filter(fn: (r) => r._measurement == "daily_quotes")
    |> filter(fn: (r) => r._field == "close")
    |> filter(fn: (r) => r.symbol == "BTC")
    |> rename(columns: {_value: "btc_close"})

eth_data =
  from(bucket: "crypto_raw")
    |> range(start: 2020-01-01T00:00:00Z, stop: 2020-12-31T23:59:59Z)
    |> filter(fn: (r) => r._measurement == "daily_quotes")
    |> filter(fn: (r) => r._field == "close")
    |> filter(fn: (r) => r.symbol == "ETH")
    |> rename(columns: {_value: "eth_close"})

join(
  tables: {btc: btc_data, eth: eth_data},
  on: ["_time"]
)
|> map(fn: (r) => ({
    r with
    ratio: r.btc_close / r.eth_close
}))

"""

        query_api = client.query_api()

        print("[INFO] Ejecutando consulta BTC/ETH ratio...")
        tables = query_api.query(query=ejer, org=ORG)

        for table in tables:
            for record in table.records:
                print(
                    f"Time: {record.get_time()} | "
                    f"BTC: {record['btc_close']} | "
                    f"ETH: {record['eth_close']} | "
                    f"Ratio: {record['ratio']}"
                )

    else:
        print(f"[ERROR] Conexión fallida. Estado: {health.status}")
        print(f"[INFO] Mensaje: {health.message}")

except (InfluxDBError, NewConnectionError) as e:
    print("[ERROR] Error al conectar con InfluxDB:")
    print(f"Detalle: {e}")

finally:
    if client:
        client.close()
        print("--- Conexión Cerrada ---")
```

    --- Iniciando conexión a InfluxDB ---
    Verificando estado de salud de InfluxDB en http://influxdb-influxdb2-1:8086
    [INFO] ¡Conexión Exitosa!
    [INFO] Versión del servidor: v2.7.12
    [INFO] Ejecutando consulta BTC/ETH ratio...
    Time: 2020-01-01 23:59:59+00:00 | BTC: 7200.17439274 | ETH: 130.802008077 | Ratio: 55.04635975084901
    Time: 2020-01-02 23:59:59+00:00 | BTC: 6985.47000061 | ETH: 127.410182379 | Ratio: 54.826622724946034
    Time: 2020-01-03 23:59:59+00:00 | BTC: 7344.88418341 | ETH: 134.171712485 | Ratio: 54.74241960078684
    Time: 2020-01-04 23:59:59+00:00 | BTC: 7410.65656642 | ETH: 135.069371268 | Ratio: 54.865559059396446
    Time: 2020-01-05 23:59:59+00:00 | BTC: 7411.31732676 | ETH: 136.276776707 | Ratio: 54.38430160917732
    Time: 2020-01-06 23:59:59+00:00 | BTC: 7769.21903905 | ETH: 144.30415371 | Ratio: 53.83919200734419
    Time: 2020-01-07 23:59:59+00:00 | BTC: 8163.69223944 | ETH: 143.543998337 | Ratio: 56.87240382056238
    Time: 2020-01-08 23:59:59+00:00 | BTC: 8079.86277673 | ETH: 141.258134415 | Ratio: 57.199274294479224
    Time: 2020-01-09 23:59:59+00:00 | BTC: 7879.07152428 | ETH: 138.979196656 | Ratio: 56.692452639384605
    Time: 2020-01-10 23:59:59+00:00 | BTC: 8166.55414039 | ETH: 143.963781218 | Ratio: 56.72644932841569
    Time: 2020-01-11 23:59:59+00:00 | BTC: 8037.53738872 | ETH: 142.927114494 | Ratio: 56.23521762945415
    Time: 2020-01-12 23:59:59+00:00 | BTC: 8192.49400532 | ETH: 145.873931189 | Ratio: 56.16146722408875
    Time: 2020-01-13 23:59:59+00:00 | BTC: 8144.19451744 | ETH: 144.226591141 | Ratio: 56.4680510924508
    Time: 2020-01-14 23:59:59+00:00 | BTC: 8827.76442606 | ETH: 165.955358611 | Ratio: 53.19360881110391
    Time: 2020-01-15 23:59:59+00:00 | BTC: 8807.01027532 | ETH: 166.230685102 | Ratio: 52.98065318034378
    Time: 2020-01-16 23:59:59+00:00 | BTC: 8723.78576573 | ETH: 164.391010988 | Ratio: 53.06729189935334
    Time: 2020-01-17 23:59:59+00:00 | BTC: 8929.0376776 | ETH: 170.77995796 | Ratio: 52.28387326158819
    Time: 2020-01-18 23:59:59+00:00 | BTC: 8942.80890321 | ETH: 175.36567147 | Ratio: 50.99520806008978
    Time: 2020-01-19 23:59:59+00:00 | BTC: 8706.24512993 | ETH: 166.969841975 | Ratio: 52.142620649024536
    Time: 2020-01-20 23:59:59+00:00 | BTC: 8657.64293942 | ETH: 167.120509335 | Ratio: 51.80479029097138
    Time: 2020-01-21 23:59:59+00:00 | BTC: 8745.89478833 | ETH: 169.69716391 | Ratio: 51.5382495901254
    Time: 2020-01-22 23:59:59+00:00 | BTC: 8680.87604222 | ETH: 168.294161709 | Ratio: 51.581563816992265
    Time: 2020-01-23 23:59:59+00:00 | BTC: 8406.5160678 | ETH: 162.928558428 | Ratio: 51.596332459511295
    Time: 2020-01-24 23:59:59+00:00 | BTC: 8445.43428152 | ETH: 163.051182861 | Ratio: 51.79621596931114
    Time: 2020-01-25 23:59:59+00:00 | BTC: 8367.84777344 | ETH: 161.283936353 | Ratio: 51.882710471087485
    Time: 2020-01-26 23:59:59+00:00 | BTC: 8596.82983316 | ETH: 168.077100489 | Ratio: 51.14813266143075
    Time: 2020-01-27 23:59:59+00:00 | BTC: 8909.81917753 | ETH: 170.930890433 | Ratio: 52.12527211997642
    Time: 2020-01-28 23:59:59+00:00 | BTC: 9358.59031703 | ETH: 176.370320541 | Ratio: 53.06216084612973
    Time: 2020-01-29 23:59:59+00:00 | BTC: 9316.62950445 | ETH: 175.050337929 | Ratio: 53.222573658948335
    Time: 2020-01-30 23:59:59+00:00 | BTC: 9508.9935947 | ETH: 184.690476436 | Ratio: 51.486106799855
    Time: 2020-01-31 23:59:59+00:00 | BTC: 9350.52936518 | ETH: 180.160175239 | Ratio: 51.90120043331226
    Time: 2020-02-01 23:59:59+00:00 | BTC: 9392.87536841 | ETH: 183.673947121 | Ratio: 51.13885510514019
    Time: 2020-02-02 23:59:59+00:00 | BTC: 9344.36529292 | ETH: 188.617538168 | Ratio: 49.54133843374127
    Time: 2020-02-03 23:59:59+00:00 | BTC: 9293.52108908 | ETH: 189.865063235 | Ratio: 48.94803146367804
    Time: 2020-02-04 23:59:59+00:00 | BTC: 9180.9629665 | ETH: 189.250602393 | Ratio: 48.51219943508927
    Time: 2020-02-05 23:59:59+00:00 | BTC: 9613.42428895 | ETH: 204.230244698 | Ratio: 47.07150159451453
    Time: 2020-02-06 23:59:59+00:00 | BTC: 9729.80223149 | ETH: 212.339079745 | Ratio: 45.82200432993593
    Time: 2020-02-07 23:59:59+00:00 | BTC: 9795.94377253 | ETH: 222.72606629 | Ratio: 43.98202660201977
    Time: 2020-02-08 23:59:59+00:00 | BTC: 9865.11946905 | ETH: 223.146521744 | Ratio: 44.209156351392934
    Time: 2020-02-09 23:59:59+00:00 | BTC: 10116.673759 | ETH: 228.578569991 | Ratio: 44.25906487820941
    Time: 2020-02-10 23:59:59+00:00 | BTC: 9856.61149362 | ETH: 223.52269963 | Ratio: 44.096691342471146
    Time: 2020-02-11 23:59:59+00:00 | BTC: 10208.2362609 | ETH: 235.851199501 | Ratio: 43.28252848617256
    Time: 2020-02-12 23:59:59+00:00 | BTC: 10326.0545246 | ETH: 265.406126106 | Ratio: 38.906617100751845
    Time: 2020-02-13 23:59:59+00:00 | BTC: 10214.3794638 | ETH: 268.099256044 | Ratio: 38.09924583350441
    Time: 2020-02-14 23:59:59+00:00 | BTC: 10312.1160909 | ETH: 284.217509609 | Ratio: 36.282479939699876
    Time: 2020-02-15 23:59:59+00:00 | BTC: 9889.42462838 | ETH: 264.728585265 | Ratio: 37.356844628170535
    Time: 2020-02-16 23:59:59+00:00 | BTC: 9934.43339025 | ETH: 259.894703492 | Ratio: 38.22483973997492
    Time: 2020-02-17 23:59:59+00:00 | BTC: 9690.14261814 | ETH: 266.363446303 | Ratio: 36.37940097500106
    Time: 2020-02-18 23:59:59+00:00 | BTC: 10141.9963705 | ETH: 281.944579134 | Ratio: 35.97159555842996
    Time: 2020-02-19 23:59:59+00:00 | BTC: 9633.38688518 | ETH: 259.763962739 | Ratio: 37.085155244799004
    Time: 2020-02-20 23:59:59+00:00 | BTC: 9608.47590343 | ETH: 257.949455024 | Ratio: 37.24945223294236
    Time: 2020-02-21 23:59:59+00:00 | BTC: 9686.44119763 | ETH: 265.600612524 | Ratio: 36.46995052300462
    Time: 2020-02-22 23:59:59+00:00 | BTC: 9663.18182933 | ETH: 262.331720974 | Ratio: 36.83573527994248
    Time: 2020-02-23 23:59:59+00:00 | BTC: 9924.51522822 | ETH: 273.754156046 | Ratio: 36.25338651133517
    Time: 2020-02-24 23:59:59+00:00 | BTC: 9650.17480677 | ETH: 265.216417336 | Ratio: 36.38603863102596
    Time: 2020-02-25 23:59:59+00:00 | BTC: 9341.70516876 | ETH: 247.817592279 | Ratio: 37.695891897145245
    Time: 2020-02-26 23:59:59+00:00 | BTC: 8820.52220005 | ETH: 225.680265514 | Ratio: 39.08415376931937
    Time: 2020-02-27 23:59:59+00:00 | BTC: 8784.49384867 | ETH: 226.753395276 | Ratio: 38.74029686734207
    Time: 2020-02-28 23:59:59+00:00 | BTC: 8672.45534996 | ETH: 226.760501479 | Ratio: 38.24499987165157
    Time: 2020-02-29 23:59:59+00:00 | BTC: 8599.50861972 | ETH: 219.84851255 | Ratio: 39.11560974406965
    Time: 2020-03-01 23:59:59+00:00 | BTC: 8562.45405008 | ETH: 218.970599927 | Ratio: 39.10321318448474
    Time: 2020-03-02 23:59:59+00:00 | BTC: 8869.67031078 | ETH: 230.569781825 | Ratio: 38.46848550827005
    Time: 2020-03-03 23:59:59+00:00 | BTC: 8787.78645576 | ETH: 224.479622332 | Ratio: 39.14736831997639
    Time: 2020-03-04 23:59:59+00:00 | BTC: 8755.24589461 | ETH: 224.517976367 | Ratio: 38.995745624833894
    Time: 2020-03-05 23:59:59+00:00 | BTC: 9078.76279174 | ETH: 229.26818886 | Ratio: 39.59887691738972
    Time: 2020-03-06 23:59:59+00:00 | BTC: 9122.54557333 | ETH: 243.525299741 | Ratio: 37.46036072240639
    Time: 2020-03-07 23:59:59+00:00 | BTC: 8909.9536515 | ETH: 237.853095033 | Ratio: 37.459902088992465
    Time: 2020-03-08 23:59:59+00:00 | BTC: 8108.11629101 | ETH: 200.689052256 | Ratio: 40.40138811691255
    Time: 2020-03-09 23:59:59+00:00 | BTC: 7923.6447033 | ETH: 201.986327111 | Ratio: 39.228619167601494
    Time: 2020-03-10 23:59:59+00:00 | BTC: 7909.72939346 | ETH: 200.767247427 | Ratio: 39.3975087810875
    Time: 2020-03-11 23:59:59+00:00 | BTC: 7911.43012933 | ETH: 194.868528471 | Ratio: 40.598808804097715
    Time: 2020-03-12 23:59:59+00:00 | BTC: 4970.78790105 | ETH: 112.347123759 | Ratio: 44.244905741539256
    Time: 2020-03-13 23:59:59+00:00 | BTC: 5563.70689169 | ETH: 133.201807239 | Ratio: 41.7690045429129
    Time: 2020-03-14 23:59:59+00:00 | BTC: 5200.36626392 | ETH: 123.306024593 | Ratio: 42.174470234402655
    Time: 2020-03-15 23:59:59+00:00 | BTC: 5392.31488002 | ETH: 125.214304313 | Ratio: 43.06468745408474
    Time: 2020-03-16 23:59:59+00:00 | BTC: 5014.47997748 | ETH: 110.605876012 | Ratio: 45.33646998045531
    Time: 2020-03-17 23:59:59+00:00 | BTC: 5225.62919259 | ETH: 113.942750228 | Ratio: 45.861883991157754
    Time: 2020-03-18 23:59:59+00:00 | BTC: 5238.43857664 | ETH: 114.842273039 | Ratio: 45.61420144358381
    Time: 2020-03-19 23:59:59+00:00 | BTC: 6191.19295222 | ETH: 136.593857971 | Ratio: 45.32555888079858
    Time: 2020-03-20 23:59:59+00:00 | BTC: 6198.77820508 | ETH: 132.737170068 | Ratio: 46.69964111713715
    Time: 2020-03-21 23:59:59+00:00 | BTC: 6185.06651501 | ETH: 132.818707849 | Ratio: 46.56773594004339
    Time: 2020-03-22 23:59:59+00:00 | BTC: 5830.25479765 | ETH: 123.321147745 | Ratio: 47.27700726322817
    Time: 2020-03-23 23:59:59+00:00 | BTC: 6416.31475839 | ETH: 134.911612009 | Ratio: 47.55939583586004
    Time: 2020-03-24 23:59:59+00:00 | BTC: 6734.80378045 | ETH: 138.761445013 | Ratio: 48.53512284928312
    Time: 2020-03-25 23:59:59+00:00 | BTC: 6681.06312656 | ETH: 136.195892908 | Ratio: 49.05480616124777
    Time: 2020-03-26 23:59:59+00:00 | BTC: 6716.44054866 | ETH: 138.361557339 | Ratio: 48.54267816749151
    Time: 2020-03-27 23:59:59+00:00 | BTC: 6469.79813509 | ETH: 133.937940192 | Ratio: 48.304447013411924
    Time: 2020-03-28 23:59:59+00:00 | BTC: 6242.1938684 | ETH: 130.986494884 | Ratio: 47.65524777136764
    Time: 2020-03-29 23:59:59+00:00 | BTC: 5922.0431227 | ETH: 125.583730441 | Ratio: 47.15613321808601
    Time: 2020-03-30 23:59:59+00:00 | BTC: 6429.84193389 | ETH: 132.904538063 | Ratio: 48.37940094146445
    Time: 2020-03-31 23:59:59+00:00 | BTC: 6438.64476637 | ETH: 133.593565057 | Ratio: 48.19577023506215
    Time: 2020-04-01 23:59:59+00:00 | BTC: 6606.77626829 | ETH: 135.634552336 | Ratio: 48.71012698831635
    Time: 2020-04-02 23:59:59+00:00 | BTC: 6793.62459642 | ETH: 142.029147631 | Ratio: 47.83260837465724
    Time: 2020-04-03 23:59:59+00:00 | BTC: 6733.3873906 | ETH: 142.091309874 | Ratio: 47.387749444852446
    Time: 2020-04-04 23:59:59+00:00 | BTC: 6867.52731596 | ETH: 145.219384622 | Ratio: 47.2907066355906
    Time: 2020-04-05 23:59:59+00:00 | BTC: 6791.12944093 | ETH: 143.54664871 | Ratio: 47.30956453500892
    Time: 2020-04-06 23:59:59+00:00 | BTC: 7271.7811527 | ETH: 169.135884595 | Ratio: 42.99372170555325
    Time: 2020-04-07 23:59:59+00:00 | BTC: 7176.41450049 | ETH: 165.101942525 | Ratio: 43.46656611507364
    Time: 2020-04-08 23:59:59+00:00 | BTC: 7334.09845346 | ETH: 172.641733789 | Ratio: 42.48160796637747
    Time: 2020-04-09 23:59:59+00:00 | BTC: 7302.0895105 | ETH: 170.807147486 | Ratio: 42.75049152201612
    Time: 2020-04-10 23:59:59+00:00 | BTC: 6865.49337195 | ETH: 158.412448608 | Ratio: 43.33935515976416
    Time: 2020-04-11 23:59:59+00:00 | BTC: 6859.08296343 | ETH: 158.216023679 | Ratio: 43.352644087088166
    Time: 2020-04-12 23:59:59+00:00 | BTC: 6971.09159108 | ETH: 161.142420145 | Ratio: 43.260437473926714
    Time: 2020-04-13 23:59:59+00:00 | BTC: 6845.03769683 | ETH: 156.279549094 | Ratio: 43.79995806561231
    Time: 2020-04-14 23:59:59+00:00 | BTC: 6842.42786097 | ETH: 157.596395681 | Ratio: 43.41741339579971
    Time: 2020-04-15 23:59:59+00:00 | BTC: 6642.10989286 | ETH: 153.286892905 | Ratio: 43.331231829302375
    Time: 2020-04-16 23:59:59+00:00 | BTC: 7116.80421777 | ETH: 172.157382821 | Ratio: 41.33894289720744
    Time: 2020-04-17 23:59:59+00:00 | BTC: 7096.18465879 | ETH: 171.638582707 | Ratio: 41.34376168150795
    Time: 2020-04-18 23:59:59+00:00 | BTC: 7257.66485847 | ETH: 186.914005844 | Ratio: 38.82889795068277
    Time: 2020-04-19 23:59:59+00:00 | BTC: 7189.42482356 | ETH: 181.614959142 | Ratio: 39.586082872935464
    Time: 2020-04-20 23:59:59+00:00 | BTC: 6881.95869275 | ETH: 172.297157575 | Ratio: 39.94238088201961
    Time: 2020-04-21 23:59:59+00:00 | BTC: 6880.32347375 | ETH: 172.737700531 | Ratio: 39.831047030264465
    Time: 2020-04-22 23:59:59+00:00 | BTC: 7117.20747869 | ETH: 182.599574801 | Ratio: 38.97713062282018
    Time: 2020-04-23 23:59:59+00:00 | BTC: 7429.72464927 | ETH: 185.028670833 | Ratio: 40.154450744424324
    Time: 2020-04-24 23:59:59+00:00 | BTC: 7550.90102725 | ETH: 189.236941873 | Ratio: 39.9018339258385
    Time: 2020-04-25 23:59:59+00:00 | BTC: 7569.93603405 | ETH: 195.515300681 | Ratio: 38.71787020086474
    Time: 2020-04-26 23:59:59+00:00 | BTC: 7679.86720422 | ETH: 197.317530184 | Ratio: 38.921362927351005
    Time: 2020-04-27 23:59:59+00:00 | BTC: 7795.60083451 | ETH: 197.2247212 | Ratio: 39.5264893116756
    Time: 2020-04-28 23:59:59+00:00 | BTC: 7807.05845106 | ETH: 198.415382994 | Ratio: 39.34704221646001
    Time: 2020-04-29 23:59:59+00:00 | BTC: 8801.03776688 | ETH: 216.968223855 | Ratio: 40.563717628816185
    Time: 2020-04-30 23:59:59+00:00 | BTC: 8658.55417975 | ETH: 207.602055895 | Ratio: 41.70745873600251
    Time: 2020-05-01 23:59:59+00:00 | BTC: 8864.76680793 | ETH: 214.219106382 | Ratio: 41.38177475225838
    Time: 2020-05-02 23:59:59+00:00 | BTC: 8988.5962069 | ETH: 215.32538422 | Ratio: 41.74424784825307
    Time: 2020-05-03 23:59:59+00:00 | BTC: 8897.46850985 | ETH: 210.93315693 | Ratio: 42.18145994374276
    Time: 2020-05-04 23:59:59+00:00 | BTC: 8912.65460539 | ETH: 208.174010942 | Ratio: 42.81348360950389
    Time: 2020-05-05 23:59:59+00:00 | BTC: 9003.07017834 | ETH: 206.774404531 | Ratio: 43.54054457929895
    Time: 2020-05-06 23:59:59+00:00 | BTC: 9268.76208066 | ETH: 204.055782253 | Ratio: 45.42268774901983
    Time: 2020-05-07 23:59:59+00:00 | BTC: 9951.5187451 | ETH: 212.289405787 | Ratio: 46.877133167374495
    Time: 2020-05-08 23:59:59+00:00 | BTC: 9842.66636785 | ETH: 212.991579806 | Ratio: 46.21152806517064
    Time: 2020-05-09 23:59:59+00:00 | BTC: 9593.89673363 | ETH: 211.600123566 | Ratio: 45.33975014734609
    Time: 2020-05-10 23:59:59+00:00 | BTC: 8756.43114193 | ETH: 188.599570436 | Ratio: 46.42869080606648
    Time: 2020-05-11 23:59:59+00:00 | BTC: 8601.79620238 | ETH: 185.91283695 | Ratio: 46.26789813708987
    Time: 2020-05-12 23:59:59+00:00 | BTC: 8804.47781074 | ETH: 189.312502269 | Ratio: 46.50764056897545
    Time: 2020-05-13 23:59:59+00:00 | BTC: 9269.98770576 | ETH: 199.193283428 | Ratio: 46.53765200426907
    Time: 2020-05-14 23:59:59+00:00 | BTC: 9733.72147137 | ETH: 202.949100772 | Ratio: 47.961392459211716
    Time: 2020-05-15 23:59:59+00:00 | BTC: 9328.19722645 | ETH: 195.622658341 | Ratio: 47.68464607095532
    Time: 2020-05-16 23:59:59+00:00 | BTC: 9377.0140257 | ETH: 200.677118596 | Ratio: 46.72687195881886
    Time: 2020-05-17 23:59:59+00:00 | BTC: 9670.73937122 | ETH: 207.158694333 | Ratio: 46.682758849959924
    Time: 2020-05-18 23:59:59+00:00 | BTC: 9726.5748149 | ETH: 214.525055208 | Ratio: 45.34004107571151
    Time: 2020-05-19 23:59:59+00:00 | BTC: 9729.0379192 | ETH: 213.451110911 | Ratio: 45.57970149547075
    Time: 2020-05-20 23:59:59+00:00 | BTC: 9522.98115678 | ETH: 210.096735593 | Ratio: 45.326649792541026
    Time: 2020-05-21 23:59:59+00:00 | BTC: 9081.76202252 | ETH: 199.883605552 | Ratio: 45.435252168079224
    Time: 2020-05-22 23:59:59+00:00 | BTC: 9182.57751787 | ETH: 207.169194624 | Ratio: 44.32404892308358
    Time: 2020-05-23 23:59:59+00:00 | BTC: 9209.28742769 | ETH: 208.694402844 | Ratio: 44.128099758257456
    Time: 2020-05-24 23:59:59+00:00 | BTC: 8790.36800074 | ETH: 202.370350969 | Ratio: 43.43703491469731
    Time: 2020-05-25 23:59:59+00:00 | BTC: 8906.93476142 | ETH: 205.319750096 | Ratio: 43.38079876512339
    Time: 2020-05-26 23:59:59+00:00 | BTC: 8835.05306073 | ETH: 201.902309998 | Ratio: 43.75904892231059
    Time: 2020-05-27 23:59:59+00:00 | BTC: 9181.01794762 | ETH: 208.863429364 | Ratio: 43.95703917903041
    Time: 2020-05-28 23:59:59+00:00 | BTC: 9525.7510947 | ETH: 219.840431324 | Ratio: 43.33029660345318
    Time: 2020-05-29 23:59:59+00:00 | BTC: 9439.12439045 | ETH: 220.675124275 | Ratio: 42.77384875826417
    Time: 2020-05-30 23:59:59+00:00 | BTC: 9700.41407169 | ETH: 242.345590189 | Ratio: 40.027194487528575
    Time: 2020-05-31 23:59:59+00:00 | BTC: 9461.05891806 | ETH: 230.975700856 | Ratio: 40.96127377467478
    Time: 2020-06-01 23:59:59+00:00 | BTC: 10167.2681012 | ETH: 246.991760327 | Ratio: 41.16440195308232
    Time: 2020-06-02 23:59:59+00:00 | BTC: 9529.80414872 | ETH: 237.219061533 | Ratio: 40.17301176024715
    Time: 2020-06-03 23:59:59+00:00 | BTC: 9656.71776526 | ETH: 244.179324047 | Ratio: 39.54764721767049
    Time: 2020-06-04 23:59:59+00:00 | BTC: 9800.63659532 | ETH: 244.426387575 | Ratio: 40.096475231475424
    Time: 2020-06-05 23:59:59+00:00 | BTC: 9665.53278908 | ETH: 241.221991758 | Ratio: 40.069036486427436
    Time: 2020-06-06 23:59:59+00:00 | BTC: 9653.67926335 | ETH: 241.931320121 | Ratio: 39.90256101823357
    Time: 2020-06-07 23:59:59+00:00 | BTC: 9758.8524174 | ETH: 245.167259144 | Ratio: 39.80487627700768
    Time: 2020-06-08 23:59:59+00:00 | BTC: 9771.48948366 | ETH: 246.309898559 | Ratio: 39.67152575201674
    Time: 2020-06-09 23:59:59+00:00 | BTC: 9795.70019463 | ETH: 244.911453825 | Ratio: 39.99690517385707
    Time: 2020-06-10 23:59:59+00:00 | BTC: 9870.09445278 | ETH: 247.444943732 | Ratio: 39.8880425840101
    Time: 2020-06-11 23:59:59+00:00 | BTC: 9321.78129819 | ETH: 231.702669421 | Ratio: 40.23165258080163
    Time: 2020-06-12 23:59:59+00:00 | BTC: 9480.84378943 | ETH: 237.493210284 | Ratio: 39.92048352916103
    Time: 2020-06-13 23:59:59+00:00 | BTC: 9475.27733834 | ETH: 238.908842797 | Ratio: 39.66063887551918
    Time: 2020-06-14 23:59:59+00:00 | BTC: 9386.78789214 | ETH: 234.114695213 | Ratio: 40.094825673372625
    Time: 2020-06-15 23:59:59+00:00 | BTC: 9450.70198692 | ETH: 229.928901759 | Ratio: 41.10271442441696
    Time: 2020-06-16 23:59:59+00:00 | BTC: 9538.0243743 | ETH: 234.416174104 | Ratio: 40.688422677133204
    Time: 2020-06-17 23:59:59+00:00 | BTC: 9480.25536624 | ETH: 233.028279483 | Ratio: 40.68285354581442
    Time: 2020-06-18 23:59:59+00:00 | BTC: 9411.84046197 | ETH: 232.101162633 | Ratio: 40.55059593498059
    Time: 2020-06-19 23:59:59+00:00 | BTC: 9288.01871603 | ETH: 227.138289785 | Ratio: 40.89147067551519
    Time: 2020-06-20 23:59:59+00:00 | BTC: 9332.340762 | ETH: 229.274256792 | Ratio: 40.703831701726536
    Time: 2020-06-21 23:59:59+00:00 | BTC: 9303.62971409 | ETH: 228.989820504 | Ratio: 40.62901003028423
    Time: 2020-06-22 23:59:59+00:00 | BTC: 9648.71760979 | ETH: 242.53319314 | Ratio: 39.78308076049767
    Time: 2020-06-23 23:59:59+00:00 | BTC: 9629.65836578 | ETH: 244.142144306 | Ratio: 39.44283521041944
    Time: 2020-06-24 23:59:59+00:00 | BTC: 9313.61034868 | ETH: 235.772462091 | Ratio: 39.50253675123972
    Time: 2020-06-25 23:59:59+00:00 | BTC: 9264.81304308 | ETH: 232.944486695 | Ratio: 39.7726221149447
    Time: 2020-06-26 23:59:59+00:00 | BTC: 9162.91760386 | ETH: 229.66803925 | Ratio: 39.89635490328679
    Time: 2020-06-27 23:59:59+00:00 | BTC: 9045.39095672 | ETH: 222.959785939 | Ratio: 40.56960728870966
    Time: 2020-06-28 23:59:59+00:00 | BTC: 9143.58219104 | ETH: 225.347168434 | Ratio: 40.57553620301196
    Time: 2020-06-29 23:59:59+00:00 | BTC: 9190.85446467 | ETH: 228.194866701 | Ratio: 40.276341871934505
    Time: 2020-06-30 23:59:59+00:00 | BTC: 9137.99340026 | ETH: 226.314997358 | Ratio: 40.37732146316808
    Time: 2020-07-01 23:59:59+00:00 | BTC: 9228.32559024 | ETH: 231.113421712 | Ratio: 39.92985574736459
    Time: 2020-07-02 23:59:59+00:00 | BTC: 9123.41015432 | ETH: 229.392201582 | Ratio: 39.77210250130795
    Time: 2020-07-03 23:59:59+00:00 | BTC: 9087.30391103 | ETH: 225.387063259 | Ratio: 40.31865795503741
    Time: 2020-07-04 23:59:59+00:00 | BTC: 9132.48795051 | ETH: 229.074112293 | Ratio: 39.866957724271266
    Time: 2020-07-05 23:59:59+00:00 | BTC: 9073.94286936 | ETH: 227.664598709 | Ratio: 39.85662646197479
    Time: 2020-07-06 23:59:59+00:00 | BTC: 9375.47475925 | ETH: 241.510225122 | Ratio: 38.82019800409667
    Time: 2020-07-07 23:59:59+00:00 | BTC: 9252.27750386 | ETH: 239.075528329 | Ratio: 38.70022820205849
    Time: 2020-07-08 23:59:59+00:00 | BTC: 9428.3330848 | ETH: 246.670015358 | Ratio: 38.22245306595681
    Time: 2020-07-09 23:59:59+00:00 | BTC: 9277.96790642 | ETH: 243.015967829 | Ratio: 38.17842913494685
    Time: 2020-07-10 23:59:59+00:00 | BTC: 9278.8078672 | ETH: 240.984985207 | Ratio: 38.503676315060616
    Time: 2020-07-11 23:59:59+00:00 | BTC: 9240.34632654 | ETH: 239.45817693 | Ratio: 38.5885604117048
    Time: 2020-07-12 23:59:59+00:00 | BTC: 9276.49985018 | ETH: 242.131695235 | Ratio: 38.31179491465059
    Time: 2020-07-13 23:59:59+00:00 | BTC: 9243.61385509 | ETH: 239.60458484 | Ratio: 38.5786184403048
    Time: 2020-07-14 23:59:59+00:00 | BTC: 9243.21341642 | ETH: 240.211494177 | Ratio: 38.47948012682995
    Time: 2020-07-15 23:59:59+00:00 | BTC: 9192.83736784 | ETH: 238.423526948 | Ratio: 38.556754383743986
    Time: 2020-07-16 23:59:59+00:00 | BTC: 9132.22786293 | ETH: 233.640883013 | Ratio: 39.08660053481254
    Time: 2020-07-17 23:59:59+00:00 | BTC: 9151.39223963 | ETH: 232.773085613 | Ratio: 39.314649352738186
    Time: 2020-07-18 23:59:59+00:00 | BTC: 9159.03990531 | ETH: 235.483805219 | Ratio: 38.894563882183284
    Time: 2020-07-19 23:59:59+00:00 | BTC: 9185.81691242 | ETH: 238.487523715 | Ratio: 38.51697048688105
    Time: 2020-07-20 23:59:59+00:00 | BTC: 9164.2313647 | ETH: 236.153167708 | Ratio: 38.806302933151585
    Time: 2020-07-21 23:59:59+00:00 | BTC: 9374.88752808 | ETH: 245.01672849 | Ratio: 38.26223452519334
    Time: 2020-07-22 23:59:59+00:00 | BTC: 9525.36344997 | ETH: 262.190656292 | Ratio: 36.32991192242055
    Time: 2020-07-23 23:59:59+00:00 | BTC: 9581.07201141 | ETH: 274.689049046 | Ratio: 34.879701410322824
    Time: 2020-07-24 23:59:59+00:00 | BTC: 9536.89268563 | ETH: 279.215409484 | Ratio: 34.15603996661401
    Time: 2020-07-25 23:59:59+00:00 | BTC: 9677.11349729 | ETH: 304.056761197 | Ratio: 31.826667689261303
    Time: 2020-07-26 23:59:59+00:00 | BTC: 9905.16724705 | ETH: 309.643609292 | Ratio: 31.98892839964681
    Time: 2020-07-27 23:59:59+00:00 | BTC: 10990.8733998 | ETH: 321.514088181 | Ratio: 34.18473343417712
    Time: 2020-07-28 23:59:59+00:00 | BTC: 10912.8230505 | ETH: 316.657252341 | Ratio: 34.46257102852728
    Time: 2020-07-29 23:59:59+00:00 | BTC: 11100.4681253 | ETH: 318.190884419 | Ratio: 34.88619149341402
    Time: 2020-07-30 23:59:59+00:00 | BTC: 11111.2142899 | ETH: 334.586629282 | Ratio: 33.20878157547391
    Time: 2020-07-31 23:59:59+00:00 | BTC: 11323.4664207 | ETH: 345.554649307 | Ratio: 32.768959825627846
    Time: 2020-08-01 23:59:59+00:00 | BTC: 11759.5927707 | ETH: 385.199719325 | Ratio: 30.528560070881614
    Time: 2020-08-02 23:59:59+00:00 | BTC: 11053.613901 | ETH: 370.671711492 | Ratio: 29.82049495093063
    Time: 2020-08-03 23:59:59+00:00 | BTC: 11246.3487749 | ETH: 386.295173437 | Ratio: 29.113355662296776
    Time: 2020-08-04 23:59:59+00:00 | BTC: 11205.8929179 | ETH: 389.875485136 | Ratio: 28.74223526516692
    Time: 2020-08-05 23:59:59+00:00 | BTC: 11747.0228312 | ETH: 401.59058634 | Ratio: 29.251240519006036
    Time: 2020-08-06 23:59:59+00:00 | BTC: 11779.7732574 | ETH: 394.961957147 | Ratio: 29.825083262425988
    Time: 2020-08-07 23:59:59+00:00 | BTC: 11601.4727146 | ETH: 379.512855039 | Ratio: 30.569380089662037
    Time: 2020-08-08 23:59:59+00:00 | BTC: 11754.0458135 | ETH: 393.987376065 | Ratio: 29.833559468059757
    Time: 2020-08-09 23:59:59+00:00 | BTC: 11675.7393433 | ETH: 391.120454943 | Ratio: 29.852029459828596
    Time: 2020-08-10 23:59:59+00:00 | BTC: 11878.1113253 | ETH: 395.887569508 | Ratio: 30.003749145399652
    Time: 2020-08-11 23:59:59+00:00 | BTC: 11410.5256775 | ETH: 380.384068285 | Ratio: 29.99738061834584
    Time: 2020-08-12 23:59:59+00:00 | BTC: 11584.9345762 | ETH: 391.024162058 | Ratio: 29.627157859573966
    Time: 2020-08-13 23:59:59+00:00 | BTC: 11784.1373895 | ETH: 428.741782282 | Ratio: 27.48539535096936
    Time: 2020-08-14 23:59:59+00:00 | BTC: 11768.8706193 | ETH: 437.397839521 | Ratio: 26.906558642786717
    Time: 2020-08-15 23:59:59+00:00 | BTC: 11865.69857 | ETH: 433.354926495 | Ratio: 27.38101690909681
    Time: 2020-08-16 23:59:59+00:00 | BTC: 11892.8040631 | ETH: 433.786609983 | Ratio: 27.41625441957758
    Time: 2020-08-17 23:59:59+00:00 | BTC: 12254.4019083 | ETH: 429.531252334 | Ratio: 28.52970963512354
    Time: 2020-08-18 23:59:59+00:00 | BTC: 11991.2332456 | ETH: 423.669315654 | Ratio: 28.30328466693334
    Time: 2020-08-19 23:59:59+00:00 | BTC: 11758.2835921 | ETH: 406.463786824 | Ratio: 28.928243974638193
    Time: 2020-08-20 23:59:59+00:00 | BTC: 11878.3716211 | ETH: 416.439794883 | Ratio: 28.52362278306583
    Time: 2020-08-21 23:59:59+00:00 | BTC: 11592.4890449 | ETH: 389.126350308 | Ratio: 29.79106666953896
    Time: 2020-08-22 23:59:59+00:00 | BTC: 11681.8255623 | ETH: 395.835141215 | Ratio: 29.511845579053713
    Time: 2020-08-23 23:59:59+00:00 | BTC: 11664.8479948 | ETH: 391.384499842 | Ratio: 29.804062244440036
    Time: 2020-08-24 23:59:59+00:00 | BTC: 11774.5958414 | ETH: 408.144207149 | Ratio: 28.849106847917316
    Time: 2020-08-25 23:59:59+00:00 | BTC: 11366.1350817 | ETH: 384.001043035 | Ratio: 29.599229710071455
    Time: 2020-08-26 23:59:59+00:00 | BTC: 11488.3634896 | ETH: 386.466124211 | Ratio: 29.726702471152855
    Time: 2020-08-27 23:59:59+00:00 | BTC: 11323.3970324 | ETH: 382.632632123 | Ratio: 29.59339084482479
    Time: 2020-08-28 23:59:59+00:00 | BTC: 11542.4997333 | ETH: 395.874666093 | Ratio: 29.15695476857921
    Time: 2020-08-29 23:59:59+00:00 | BTC: 11506.8653177 | ETH: 399.921471038 | Ratio: 28.77281204190868
    Time: 2020-08-30 23:59:59+00:00 | BTC: 11711.506161 | ETH: 428.395717595 | Ratio: 27.338056100906012
    Time: 2020-08-31 23:59:59+00:00 | BTC: 11680.8204905 | ETH: 435.079745266 | Ratio: 26.847539141033916
    Time: 2020-09-01 23:59:59+00:00 | BTC: 11970.4787405 | ETH: 477.051924154 | Ratio: 25.092611798450136
    Time: 2020-09-02 23:59:59+00:00 | BTC: 11414.0337325 | ETH: 440.040506887 | Ratio: 25.93859781965723
    Time: 2020-09-03 23:59:59+00:00 | BTC: 10245.296686 | ETH: 385.671928369 | Ratio: 26.56479751929881
    Time: 2020-09-04 23:59:59+00:00 | BTC: 10511.8138807 | ETH: 388.241140415 | Ratio: 27.075476518185777
    Time: 2020-09-05 23:59:59+00:00 | BTC: 10169.567221 | ETH: 335.260079079 | Ratio: 30.333367602062946
    Time: 2020-09-06 23:59:59+00:00 | BTC: 10280.3517032 | ETH: 353.362265679 | Ratio: 29.092952761794994
    Time: 2020-09-07 23:59:59+00:00 | BTC: 10369.5637386 | ETH: 352.673494754 | Ratio: 29.402730550627492
    Time: 2020-09-08 23:59:59+00:00 | BTC: 10131.5166457 | ETH: 337.602111896 | Ratio: 30.010228872090302
    Time: 2020-09-09 23:59:59+00:00 | BTC: 10242.3477803 | ETH: 351.110016528 | Ratio: 29.17133461922526
    Time: 2020-09-10 23:59:59+00:00 | BTC: 10363.1390401 | ETH: 368.101907072 | Ratio: 28.15290777092603
    Time: 2020-09-11 23:59:59+00:00 | BTC: 10400.9146854 | ETH: 374.695588755 | Ratio: 27.75830566876725
    Time: 2020-09-12 23:59:59+00:00 | BTC: 10442.1706031 | ETH: 387.183109613 | Ratio: 26.969592277765503
    Time: 2020-09-13 23:59:59+00:00 | BTC: 10323.7557975 | ETH: 365.570005047 | Ratio: 28.2401609950814
    Time: 2020-09-14 23:59:59+00:00 | BTC: 10680.8374328 | ETH: 377.268875067 | Ratio: 28.310942509909324
    Time: 2020-09-15 23:59:59+00:00 | BTC: 10796.9509861 | ETH: 364.83921823 | Ratio: 29.5937236092131
    Time: 2020-09-16 23:59:59+00:00 | BTC: 10974.9048915 | ETH: 365.812291316 | Ratio: 30.0014656479094
    Time: 2020-09-17 23:59:59+00:00 | BTC: 10948.9899152 | ETH: 389.019219686 | Ratio: 28.14511304618205
    Time: 2020-09-18 23:59:59+00:00 | BTC: 10944.5858045 | ETH: 384.364541978 | Ratio: 28.474493896282556
    Time: 2020-09-19 23:59:59+00:00 | BTC: 11094.3462761 | ETH: 385.544383604 | Ratio: 28.7757953374707
    Time: 2020-09-20 23:59:59+00:00 | BTC: 10938.2712894 | ETH: 371.052826188 | Ratio: 29.47901354579077
    Time: 2020-09-21 23:59:59+00:00 | BTC: 10462.2596185 | ETH: 341.78607406 | Ratio: 30.61054973428604
    Time: 2020-09-22 23:59:59+00:00 | BTC: 10538.4603213 | ETH: 344.503162317 | Ratio: 30.59031519601225
    Time: 2020-09-23 23:59:59+00:00 | BTC: 10246.18649281 | ETH: 321.11631734 | Ratio: 31.908021920795985
    Time: 2020-09-24 23:59:59+00:00 | BTC: 10760.06625677 | ETH: 349.35558514 | Ratio: 30.7997545035899
    Time: 2020-09-25 23:59:59+00:00 | BTC: 10692.71721234 | ETH: 352.18324474 | Ratio: 30.36123203485708
    Time: 2020-09-26 23:59:59+00:00 | BTC: 10750.72357903 | ETH: 355.48809037 | Ratio: 30.24214838770099
    Time: 2020-09-27 23:59:59+00:00 | BTC: 10775.26937624 | ETH: 357.43849724 | Ratio: 30.145799793369786
    Time: 2020-09-28 23:59:59+00:00 | BTC: 10709.65218175 | ETH: 355.15942359 | Ratio: 30.154492519149205
    Time: 2020-09-29 23:59:59+00:00 | BTC: 10844.64098118 | ETH: 359.75739393 | Ratio: 30.144317154160014
    Time: 2020-09-30 23:59:59+00:00 | BTC: 10784.49157795 | ETH: 359.93787376 | Ratio: 29.962091694582
    Time: 2020-10-01 23:59:59+00:00 | BTC: 10619.45190766 | ETH: 353.20591482 | Ratio: 30.065894884778086
    Time: 2020-10-02 23:59:59+00:00 | BTC: 10575.97504191 | ETH: 346.2389138 | Ratio: 30.54531024788006
    Time: 2020-10-03 23:59:59+00:00 | BTC: 10549.32889962 | ETH: 346.52208572 | Ratio: 30.44345320068334
    Time: 2020-10-04 23:59:59+00:00 | BTC: 10669.58254327 | ETH: 352.5790067 | Ratio: 30.261536678354936
    Time: 2020-10-05 23:59:59+00:00 | BTC: 10793.33942751 | ETH: 353.95677154 | Ratio: 30.493383077685422
    Time: 2020-10-06 23:59:59+00:00 | BTC: 10604.40588882 | ETH: 340.81584538 | Ratio: 31.11476779196222
    Time: 2020-10-07 23:59:59+00:00 | BTC: 10668.96895539 | ETH: 341.80866898 | Ratio: 31.213277847011735
    Time: 2020-10-08 23:59:59+00:00 | BTC: 10915.68573098 | ETH: 350.76615934 | Ratio: 31.119551987337957
    Time: 2020-10-09 23:59:59+00:00 | BTC: 11064.45759247 | ETH: 365.59047723 | Ratio: 30.264621978950338
    Time: 2020-10-10 23:59:59+00:00 | BTC: 11296.3614282 | ETH: 370.96758819 | Ratio: 30.451073861510228
    Time: 2020-10-11 23:59:59+00:00 | BTC: 11384.1819535 | ETH: 375.14204941 | Ratio: 30.34632340310645
    Time: 2020-10-12 23:59:59+00:00 | BTC: 11555.3628878 | ETH: 387.7312655 | Ratio: 29.80250476550749
    Time: 2020-10-13 23:59:59+00:00 | BTC: 11425.8994007 | ETH: 381.19076126 | Ratio: 29.974229603394562
    Time: 2020-10-14 23:59:59+00:00 | BTC: 11429.50688675 | ETH: 379.48403791 | Ratio: 30.118544510324487
    Time: 2020-10-15 23:59:59+00:00 | BTC: 11495.34965037 | ETH: 377.44184574 | Ratio: 30.455949121996788
    Time: 2020-10-16 23:59:59+00:00 | BTC: 11322.12268618 | ETH: 366.22901728 | Ratio: 30.915416725495795
    Time: 2020-10-17 23:59:59+00:00 | BTC: 11358.10156733 | ETH: 368.85594038 | Ratio: 30.79278472681975
    Time: 2020-10-18 23:59:59+00:00 | BTC: 11483.35971184 | ETH: 378.21369795 | Ratio: 30.362093636698756
    Time: 2020-10-19 23:59:59+00:00 | BTC: 11742.03715033 | ETH: 379.93560927 | Ratio: 30.905334651023878
    Time: 2020-10-20 23:59:59+00:00 | BTC: 11916.33514058 | ETH: 369.13691491 | Ratio: 32.28161329647929
    Time: 2020-10-21 23:59:59+00:00 | BTC: 12823.68918938 | ETH: 392.18996695 | Ratio: 32.69764723740341
    Time: 2020-10-22 23:59:59+00:00 | BTC: 12965.89129043 | ETH: 413.77299269 | Ratio: 31.33576023446287
    Time: 2020-10-23 23:59:59+00:00 | BTC: 12931.53902256 | ETH: 409.76669164 | Ratio: 31.55829716369672
    Time: 2020-10-24 23:59:59+00:00 | BTC: 13108.06261161 | ETH: 412.45761883 | Ratio: 31.780386670497325
    Time: 2020-10-25 23:59:59+00:00 | BTC: 13031.17431056 | ETH: 406.2177613 | Ratio: 32.079282473658786
    Time: 2020-10-26 23:59:59+00:00 | BTC: 13075.24769656 | ETH: 393.88831313 | Ratio: 33.19531770988242
    Time: 2020-10-27 23:59:59+00:00 | BTC: 13654.21844012 | ETH: 403.99704505 | Ratio: 33.79781760143842
    Time: 2020-10-28 23:59:59+00:00 | BTC: 13271.28536861 | ETH: 388.65077072 | Ratio: 34.14707075975717
    Time: 2020-10-29 23:59:59+00:00 | BTC: 13437.8832414 | ETH: 386.7301135 | Ratio: 34.7474447225843
    Time: 2020-10-30 23:59:59+00:00 | BTC: 13546.52226938 | ETH: 382.81999199 | Ratio: 35.386141144200906
    Time: 2020-10-31 23:59:59+00:00 | BTC: 13780.99470249 | ETH: 386.59033529 | Ratio: 35.64754067675337
    Time: 2020-11-01 23:59:59+00:00 | BTC: 13737.10982864 | ETH: 396.35818693 | Ratio: 34.65832240035471
    Time: 2020-11-02 23:59:59+00:00 | BTC: 13550.4893841 | ETH: 383.15673256 | Ratio: 35.365395496418884
    Time: 2020-11-03 23:59:59+00:00 | BTC: 13950.30084729 | ETH: 387.60217328 | Ratio: 35.991286450327614
    Time: 2020-11-04 23:59:59+00:00 | BTC: 14133.70715301 | ETH: 402.14199843 | Ratio: 35.14606086454366
    Time: 2020-11-05 23:59:59+00:00 | BTC: 15579.84846029 | ETH: 414.06733818 | Ratio: 37.62636417730987
    Time: 2020-11-06 23:59:59+00:00 | BTC: 15565.88058083 | ETH: 454.71929029 | Ratio: 34.23184569738127
    Time: 2020-11-07 23:59:59+00:00 | BTC: 14833.7541075 | ETH: 435.71313513 | Ratio: 34.04477145972242
    Time: 2020-11-08 23:59:59+00:00 | BTC: 15479.56703842 | ETH: 453.55478553 | Ratio: 34.129431619449015
    Time: 2020-11-09 23:59:59+00:00 | BTC: 15332.31559743 | ETH: 444.16305707 | Ratio: 34.51956517629433
    Time: 2020-11-10 23:59:59+00:00 | BTC: 15290.90268148 | ETH: 449.67962112 | Ratio: 34.003992983705885
    Time: 2020-11-11 23:59:59+00:00 | BTC: 15701.33973237 | ETH: 462.96052774 | Ratio: 33.91507221796654
    Time: 2020-11-12 23:59:59+00:00 | BTC: 16276.34394919 | ETH: 461.00527114 | Ratio: 35.30619923052275
    Time: 2020-11-13 23:59:59+00:00 | BTC: 16317.80819009 | ETH: 474.62642092 | Ratio: 34.38031991236414
    Time: 2020-11-14 23:59:59+00:00 | BTC: 16068.13870685 | ETH: 460.14983674 | Ratio: 34.919361964109605
    Time: 2020-11-15 23:59:59+00:00 | BTC: 15955.58743887 | ETH: 447.55909533 | Ratio: 35.65023614838041
    Time: 2020-11-16 23:59:59+00:00 | BTC: 16716.11132377 | ETH: 459.94031258 | Ratio: 36.34408827963405
    Time: 2020-11-17 23:59:59+00:00 | BTC: 17645.40576746 | ETH: 480.36008258 | Ratio: 36.73370541675121
    Time: 2020-11-18 23:59:59+00:00 | BTC: 17804.00563217 | ETH: 479.48406975 | Ratio: 37.13158946334317
    Time: 2020-11-19 23:59:59+00:00 | BTC: 17817.09024754 | ETH: 471.63041968 | Ratio: 37.77765280625633
    Time: 2020-11-20 23:59:59+00:00 | BTC: 18621.31436938 | ETH: 509.74457334 | Ratio: 36.53067701607403
    Time: 2020-11-21 23:59:59+00:00 | BTC: 18642.23276593 | ETH: 549.48662086 | Ratio: 33.92663635149677
    Time: 2020-11-22 23:59:59+00:00 | BTC: 18370.00252365 | ETH: 558.06809523 | Ratio: 32.91713445126989
    Time: 2020-11-23 23:59:59+00:00 | BTC: 18364.12159134 | ETH: 608.45402857 | Ratio: 30.18160901079035
    Time: 2020-11-24 23:59:59+00:00 | BTC: 19107.46444977 | ETH: 603.89774601 | Ratio: 31.640231439866305
    Time: 2020-11-25 23:59:59+00:00 | BTC: 18732.1207774 | ETH: 570.68661621 | Ratio: 32.82383053207436
    Time: 2020-11-26 23:59:59+00:00 | BTC: 17150.62357809 | ETH: 518.80117389 | Ratio: 33.058181903278424
    Time: 2020-11-27 23:59:59+00:00 | BTC: 17108.40172774 | ETH: 517.49368769 | Ratio: 33.060116740957504
    Time: 2020-11-28 23:59:59+00:00 | BTC: 17717.4150112 | ETH: 538.22980058 | Ratio: 32.91793763947592
    Time: 2020-11-29 23:59:59+00:00 | BTC: 18177.48341979 | ETH: 575.75804789 | Ratio: 31.571392682057407
    Time: 2020-11-30 23:59:59+00:00 | BTC: 19625.83502949 | ETH: 614.84252202 | Ratio: 31.920100394181254
    Time: 2020-12-01 23:59:59+00:00 | BTC: 18802.99829969 | ETH: 587.32418713 | Ratio: 32.01468407349635
    Time: 2020-12-02 23:59:59+00:00 | BTC: 19201.09115697 | ETH: 598.35234223 | Ratio: 32.08994066173358
    Time: 2020-12-03 23:59:59+00:00 | BTC: 19445.39847988 | ETH: 616.70875486 | Ratio: 31.53092659483054
    Time: 2020-12-04 23:59:59+00:00 | BTC: 18699.76561337 | ETH: 569.35419749 | Ratio: 32.84381795340753
    Time: 2020-12-05 23:59:59+00:00 | BTC: 19154.231131 | ETH: 596.59547474 | Ratio: 32.1058940974159
    Time: 2020-12-06 23:59:59+00:00 | BTC: 19345.12095871 | ETH: 601.90899244 | Ratio: 32.139611140031896
    Time: 2020-12-07 23:59:59+00:00 | BTC: 19191.63128698 | ETH: 591.84337934 | Ratio: 32.42687500936774
    Time: 2020-12-08 23:59:59+00:00 | BTC: 18321.14491611 | ETH: 554.82775708 | Ratio: 33.02132000845137
    Time: 2020-12-09 23:59:59+00:00 | BTC: 18553.91537685 | ETH: 573.47911163 | Ratio: 32.35325402544165
    Time: 2020-12-10 23:59:59+00:00 | BTC: 18264.99210672 | ETH: 559.67850106 | Ratio: 32.63479313950263
    Time: 2020-12-11 23:59:59+00:00 | BTC: 18058.90334725 | ETH: 545.79734103 | Ratio: 33.08719553886098
    Time: 2020-12-12 23:59:59+00:00 | BTC: 18803.65687045 | ETH: 568.56731778 | Ratio: 33.07199742656653
    Time: 2020-12-13 23:59:59+00:00 | BTC: 19142.3825335 | ETH: 589.6632225 | Ratio: 32.463246482190094
    Time: 2020-12-14 23:59:59+00:00 | BTC: 19246.64434137 | ETH: 586.01115197 | Ratio: 32.8434779383777
    Time: 2020-12-15 23:59:59+00:00 | BTC: 19417.07603342 | ETH: 589.35560245 | Ratio: 32.946282266091316
    Time: 2020-12-16 23:59:59+00:00 | BTC: 21310.59813054 | ETH: 636.18184867 | Ratio: 33.49765192938446
    Time: 2020-12-17 23:59:59+00:00 | BTC: 22805.16149213 | ETH: 642.86896702 | Ratio: 35.47404317530312
    Time: 2020-12-18 23:59:59+00:00 | BTC: 23137.96056165 | ETH: 654.81192689 | Ratio: 35.33527660612828
    Time: 2020-12-19 23:59:59+00:00 | BTC: 23869.83196434 | ETH: 659.29792646 | Ratio: 36.20492497603539
    Time: 2020-12-20 23:59:59+00:00 | BTC: 23477.29519711 | ETH: 638.29084637 | Ratio: 36.781500675791996
    Time: 2020-12-21 23:59:59+00:00 | BTC: 22803.0814087 | ETH: 609.81787165 | Ratio: 37.39326521704113
    Time: 2020-12-22 23:59:59+00:00 | BTC: 23783.02850288 | ETH: 634.85419947 | Ratio: 37.462189779535144
    Time: 2020-12-23 23:59:59+00:00 | BTC: 23241.34486501 | ETH: 583.71459689 | Ratio: 39.81628177338486
    Time: 2020-12-24 23:59:59+00:00 | BTC: 23735.94972763 | ETH: 611.60718693 | Ratio: 38.809141283597505
    Time: 2020-12-25 23:59:59+00:00 | BTC: 24664.79027412 | ETH: 626.41070163 | Ratio: 39.37479070829904
    Time: 2020-12-26 23:59:59+00:00 | BTC: 26437.0375091 | ETH: 635.83583086 | Ratio: 41.57840157158582
    Time: 2020-12-27 23:59:59+00:00 | BTC: 26272.29456706 | ETH: 682.6423591 | Ratio: 38.48617686382304
    Time: 2020-12-28 23:59:59+00:00 | BTC: 27084.80788628 | ETH: 730.39736483 | Ratio: 37.08229135326082
    Time: 2020-12-29 23:59:59+00:00 | BTC: 27362.4365573 | ETH: 731.52011874 | Ratio: 37.4048995459348
    Time: 2020-12-30 23:59:59+00:00 | BTC: 28840.95341968 | ETH: 751.61897194 | Ratio: 38.37177412544385
    --- Conexión Cerrada ---


## **Entrega**

Debes entregar un Markdown con el código Flux y una captura de la visualización del resultado pedido.


```python

```
