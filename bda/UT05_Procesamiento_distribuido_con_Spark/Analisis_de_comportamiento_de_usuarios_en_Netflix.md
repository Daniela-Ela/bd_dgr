# **PR0505. Análisis de comportamiento de usuarios en Netflix**

## **Contexto**

En esta práctica vamos a trabajar con el dataset **Netflix audience behaviour - IK Movies** que abarca el comportamiento en la versión web de los usuarios en Netflix UK entre enero de 2017 y junio de 2019 de forma anonimizada. Este dataset documenta cada vez que alguien hizo un click en una URL del tipo netflix.com/watch para ver una película.

Los campos que tiene el dataset son:
- ``row_id``: identificador de fila
- ``click_datetime``: fecha y hora del clic
- ``time_to_next_click``: segundos hasta el siguiente clic del usuario
- ``movie_title``: título de la película
- ``movie_genres``: género/s
- ``release_date``: fecha de estreno original
- ``title_id``: ID de la película
- ``user_id``: ID del usuario
  
Tu objetivo será utilizar funciones de ventana en PySpark para extraer insights sobre cómo los usuarios británicos navegan y consumen películas en la interfaz web de Netflix.com.


```python
from pyspark.sql import SparkSession

try:
    spark = ( SparkSession.builder
    .appName("Haciendo pruebas")
    .master("spark://spark-master:7077")
    .getOrCreate()
    )

    print("SparkSession iniciada correctamente.")
except Exception as e:
    print("Error en la conexión")
    print(e)
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/03/09 11:14:43 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


    SparkSession iniciada correctamente.



```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

schema = StructType([
    StructField("Unnamed: 0", IntegerType(), True),
    StructField("datetime", StringType(), True),       
    StructField("duration", DoubleType(), True),
    StructField("title", StringType(), True),
    StructField("genres", StringType(), True),
    StructField("release_date", StringType(), True),  
    StructField("movie_id", StringType(), True),
    StructField("user_id", StringType(), True),
])

df_pelis = (spark.read
    .format("csv")
    .schema(schema)
    .option("header", "true")
    .option("quote", '"')        
    .option("escape", '"')       
    .load("./vodclickstream_uk_movies_03.csv")
)

df_pelis.printSchema()
df_pelis.show(5, truncate=False)
```

    root
     |-- Unnamed: 0: integer (nullable = true)
     |-- datetime: string (nullable = true)
     |-- duration: double (nullable = true)
     |-- title: string (nullable = true)
     |-- genres: string (nullable = true)
     |-- release_date: string (nullable = true)
     |-- movie_id: string (nullable = true)
     |-- user_id: string (nullable = true)
    
    +----------+-------------------+--------+----------------------------------+-----------------------------------------------------+------------+----------+----------+
    |Unnamed: 0|datetime           |duration|title                             |genres                                               |release_date|movie_id  |user_id   |
    +----------+-------------------+--------+----------------------------------+-----------------------------------------------------+------------+----------+----------+
    |58773     |2017-01-01 01:15:09|0.0     |Angus, Thongs and Perfect Snogging|Comedy, Drama, Romance                               |2008-07-25  |26bd5987e8|1dea19f6fe|
    |58774     |2017-01-01 13:56:02|0.0     |The Curse of Sleeping Beauty      |Fantasy, Horror, Mystery, Thriller                   |2016-06-02  |f26ed2675e|544dcbc510|
    |58775     |2017-01-01 15:17:47|10530.0 |London Has Fallen                 |Action, Thriller                                     |2016-03-04  |f77e500e7a|7cbcc791bf|
    |58776     |2017-01-01 16:04:13|49.0    |Vendetta                          |Action, Drama                                        |2015-06-12  |c74aec7673|ebf43c36b6|
    |58777     |2017-01-01 19:16:37|0.0     |The SpongeBob SquarePants Movie   |Animation, Action, Adventure, Comedy, Family, Fantasy|2004-11-19  |a80d6fc2aa|a57c992287|
    +----------+-------------------+--------+----------------------------------+-----------------------------------------------------+------------+----------+----------+
    only showing top 5 rows
    


## **Ejercicios**

### **1.- Auditoría de telemetría Web (validación de datos)**

Supón que el equipo de ingeniería web necesita verificar si el rastreador del navegador calculó correctamente el tiempo entre clics.

Ignora la columna ``time_to_next_click original``. Crea una nueva columna ``calculated_time_to_next`` calculando tú mismo la diferencia en segundos entre el ``click_datetime`` de la fila actual y el del siguiente registro cronológico del mismo usuario (recuerda que puedes usar la función ``lead()`` para extraer información de una columna anterior).

Compara ambas columnas para ver si hay discrepancias.


```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

ventana = Window.partitionBy("user_id").orderBy("datetime")

df_pelis = df_pelis.withColumn("next_datetime",F.lead("datetime").over(ventana))

df_pelis = df_pelis.withColumn("calculated_time_to_next",
    F.unix_timestamp(F.col("next_datetime")) - F.unix_timestamp(F.col("datetime")))

df_pelis.select("user_id", "datetime", "next_datetime", "calculated_time_to_next").show(10)
```

    [Stage 2:>                                                          (0 + 8) / 8]

    +----------+-------------------+-------------------+-----------------------+
    |   user_id|           datetime|      next_datetime|calculated_time_to_next|
    +----------+-------------------+-------------------+-----------------------+
    |0006ea6b5c|2017-05-19 20:21:43|2017-05-20 21:54:34|                  91971|
    |0006ea6b5c|2017-05-20 21:54:34|2017-05-26 18:38:01|                 506607|
    |0006ea6b5c|2017-05-26 18:38:01|2017-05-26 23:31:46|                  17625|
    |0006ea6b5c|2017-05-26 23:31:46|2017-05-27 22:45:41|                  83635|
    |0006ea6b5c|2017-05-27 22:45:41|2017-06-02 22:51:18|                 518737|
    |0006ea6b5c|2017-06-02 22:51:18|2017-06-02 23:11:00|                   1182|
    |0006ea6b5c|2017-06-02 23:11:00|2017-06-03 21:54:46|                  81826|
    |0006ea6b5c|2017-06-03 21:54:46|2017-06-03 23:04:46|                   4200|
    |0006ea6b5c|2017-06-03 23:04:46|2017-06-04 23:28:04|                  87798|
    |0006ea6b5c|2017-06-04 23:28:04|2017-06-09 21:14:59|                 424015|
    +----------+-------------------+-------------------+-----------------------+
    only showing top 10 rows
    


                                                                                    

### **2.- Detección de “zapping”**

En la versión web, es muy común que los usuarios hagan clic en una película, vean los primeros segundos y vuelvan atrás si no les convence.

Identifica estos rechazos rápidos. Utiliza la función ``lead()`` (o ``lag()``) para calcular el tiempo de visualización. Si el tiempo hasta el siguiente clic del usuario en otra película es **inferior a 5 minutos** (**300 segundos**), crea una columna llamada ``es_zapping`` y márcala con un ``1`` (de lo contrario, ``0``).


```python
def ejercicio1(df_pelis):
    df_pelis = df_pelis.withColumn(
        "es_zapping",
        F.when(F.col("calculated_time_to_next") < 300, 1).otherwise(0)
    )

    df_pelis.select("calculated_time_to_next", "es_zapping", "user_id", "datetime").show(10)
    return df_pelis
```


```python
df_pelis = ejercicio1(df_pelis)
```

    [Stage 11:=======>                                                  (1 + 7) / 8]

    +-----------------------+----------+----------+-------------------+
    |calculated_time_to_next|es_zapping|   user_id|           datetime|
    +-----------------------+----------+----------+-------------------+
    |                  91971|         0|0006ea6b5c|2017-05-19 20:21:43|
    |                 506607|         0|0006ea6b5c|2017-05-20 21:54:34|
    |                  17625|         0|0006ea6b5c|2017-05-26 18:38:01|
    |                  83635|         0|0006ea6b5c|2017-05-26 23:31:46|
    |                 518737|         0|0006ea6b5c|2017-05-27 22:45:41|
    |                   1182|         0|0006ea6b5c|2017-06-02 22:51:18|
    |                  81826|         0|0006ea6b5c|2017-06-02 23:11:00|
    |                   4200|         0|0006ea6b5c|2017-06-03 21:54:46|
    |                  87798|         0|0006ea6b5c|2017-06-03 23:04:46|
    |                 424015|         0|0006ea6b5c|2017-06-04 23:28:04|
    +-----------------------+----------+----------+-------------------+
    only showing top 10 rows
    


                                                                                    

### **3.- El ranking de “maratones”**

Queremos saber cuántas películas llega a iniciar un usuario web en un solo día.

1. Extrae solo la fecha (sin la hora) de la columna ``click_datetime``.
2. Utiliza ``row_number()`` particionando por ``user_id`` y por la fecha, ordenando por ``click_datetime``.
3. Esto creará un contador diario (``pelicula_nro_1``, ``pelicula_nro_2``…). Filtra el DataFrame final para encontrar a los usuarios extremos que hayan iniciado más de 5 películas en un mismo día.


```python
df_pelis = df_pelis.withColumn("click_date", F.to_date("datetime"))

ventana = Window.partitionBy("user_id","click_date").orderBy("datetime")

df_pelis = df_pelis.withColumn(
    "pelicula_nro_dia",
    F.row_number().over(ventana)
)

ventana2 = Window.partitionBy("user_id","click_date")

df_pelis = df_pelis.withColumn(
    "Mayor_veces_vista",
    F.max("pelicula_nro_dia").over(ventana2)
)

df_pelis.filter(F.col("Mayor_veces_vista") > 5) \
.select("user_id","click_date","Mayor_veces_vista") \
.distinct() \
.show(100)
```

    [Stage 49:=======>                                                  (1 + 7) / 8]

    +----------+----------+-----------------+
    |   user_id|click_date|Mayor_veces_vista|
    +----------+----------+-----------------+
    |00b88bd923|2017-10-23|                9|
    |0141ae3d9a|2019-02-20|                6|
    |015d339273|2019-01-20|                6|
    |020c9c652a|2019-01-20|                6|
    |023d43562c|2017-05-28|                6|
    |0244e5d9eb|2017-08-22|                8|
    |02751be82b|2017-07-22|                6|
    |02a445c1b1|2017-06-12|                7|
    |02bbf94ed5|2017-04-08|                6|
    |02c54679dd|2018-04-06|                6|
    |02cd2456b2|2018-03-30|                8|
    |032898773f|2018-02-16|                6|
    |036344729a|2017-02-26|                7|
    |03da9f71f4|2017-04-20|                7|
    |04c6fce5ff|2018-11-19|                6|
    |04e88dad2b|2018-12-02|               10|
    |05225d37e3|2019-05-24|                6|
    |05278fd7d2|2017-06-28|               10|
    |0532fd265d|2018-09-30|                8|
    |0565211f70|2019-01-01|                8|
    |058a832d8a|2019-04-27|                7|
    |062d063205|2017-03-18|               13|
    |06794754e8|2017-08-11|                7|
    |06824f04c4|2019-01-13|                7|
    |07707aeaf0|2017-05-16|                8|
    |07aec1a306|2018-10-28|                8|
    |07b2842b0b|2017-12-10|                8|
    |07d5f6755a|2018-01-16|                7|
    |08263521af|2018-12-20|                7|
    |085bdc1fcf|2019-02-02|                8|
    |086dae4fd1|2018-08-20|                6|
    |0875968181|2018-09-29|                7|
    |087627a780|2018-09-30|                6|
    |087d55751b|2018-01-22|               10|
    |08a1b7e49c|2018-02-11|               11|
    |0911f0fa1d|2017-10-22|                6|
    |0916f2d43f|2018-08-16|               24|
    |092663d06c|2018-12-19|               17|
    |09b10da29e|2018-01-23|                7|
    |09d01ca26c|2017-08-07|                8|
    |09f28d64cc|2017-01-16|                6|
    |0a345be2dd|2017-08-19|                6|
    |0c5c56ea4e|2018-11-26|               10|
    |0c711cdd1c|2018-01-29|               13|
    |0ca1127042|2018-02-17|               10|
    |0d69cf00ba|2018-07-26|               10|
    |0da06623d4|2017-04-25|                7|
    |0da6734c9b|2017-06-17|                6|
    |0defe35eaf|2019-04-11|                7|
    |0e09a98719|2018-05-25|                7|
    |0e0a2fa16d|2018-08-26|                6|
    |0e55723d9f|2019-06-02|                7|
    |0f89fb1178|2017-10-01|                7|
    |0fce1b1e65|2018-04-03|                9|
    |0ff3168e8a|2019-05-16|                6|
    |0ffc6ff4e8|2017-07-12|                6|
    |10268ed598|2017-06-08|                8|
    |107bcc10cf|2018-04-01|                7|
    |10ebd502bb|2017-03-21|                6|
    |1111f33ccb|2017-02-26|                6|
    |115ed90066|2019-04-28|                7|
    |11c844cdaa|2019-04-15|                6|
    |11e22d75df|2017-02-07|                7|
    |11f1ac2cb4|2017-04-18|                6|
    |1282fabbab|2018-02-19|                6|
    |1298f49f8f|2017-08-21|                6|
    |1341c3b1d2|2019-04-17|                6|
    |13df4b2d14|2019-06-07|               11|
    |13f26cf453|2017-06-26|                8|
    |148ae335aa|2018-12-13|                6|
    |1535136487|2019-01-01|                6|
    |15462061df|2017-05-05|                6|
    |157e99b3b0|2017-11-14|                8|
    |1589b4a147|2017-12-14|                6|
    |15910db3db|2019-06-29|                6|
    |15ab589c02|2019-01-07|                8|
    |15fa7b3d17|2019-06-19|                7|
    |162f321275|2017-04-24|                8|
    |16d994f6dd|2017-11-11|               37|
    |16dedc980b|2019-06-08|                6|
    |170474b06a|2017-09-04|                7|
    |170ce84940|2019-01-15|               15|
    |1717af2439|2019-05-05|                6|
    |171f216f35|2017-05-26|                7|
    |17aa9aadcd|2019-06-12|                7|
    |182a9746fe|2019-02-16|                6|
    |18609b13d0|2017-12-10|                9|
    |1862bb7dc9|2019-06-24|                7|
    |187869679d|2017-08-28|                8|
    |18c10ac8e5|2017-01-02|               20|
    |1935368ac5|2019-03-03|               11|
    |1935368ac5|2019-04-19|                6|
    |19c85d5383|2018-08-30|                8|
    |19d5ec8832|2018-12-12|                8|
    |1a1671a24d|2018-08-09|                6|
    |1aeb405fe3|2018-02-22|                6|
    |1b1e61b7d1|2019-01-01|                6|
    |1b2c825fa6|2018-03-09|                8|
    |1bee84b977|2018-06-22|                6|
    |1c7b7f3c6b|2018-03-04|                6|
    +----------+----------+-----------------+
    only showing top 100 rows
    


                                                                                    

### **4.- Análisis de re-visualización**

Queremos identificar las películas que los usuarios del Reino Unido ven repetidas veces en sus ordenadores.

Crea una columna llamada ``veces_vista_por_usuario`` que cuente cuántas veces un mismo user_id ha hecho clic en el mismo ``title_id`` a lo largo de todo el periodo (2017-2019). Usa la función ``count()`` sobre una ventana particionada por usuario y película. Luego, filtra para mostrar solo aquellos registros donde el usuario haya visto la misma película 3 veces o más.


```python
ventana_user_movie = Window.partitionBy("user_id","movie_id")

df_pelis = df_pelis.withColumn(
    "veces_vista_por_usuario",
    F.count("*").over(ventana_user_movie)
)

df_pelis.filter(F.col("veces_vista_por_usuario") >= 3) \
.orderBy("veces_vista_por_usuario", ascending=False) \
.select("user_id","movie_id","title","veces_vista_por_usuario") \
.distinct() \
.show(10)
```

    [Stage 46:=======>                                                  (1 + 7) / 8]

    +----------+----------+--------------------+-----------------------+
    |   user_id|  movie_id|               title|veces_vista_por_usuario|
    +----------+----------+--------------------+-----------------------+
    |000118a755|4c3d7b724e|From Dusk till Da...|                      3|
    |000296842d|e847f14da5|Black Mirror: Ban...|                      8|
    |0016c962c8|510b52ee06|Approaching the U...|                      3|
    |0023e9b95e|bf9b17da5d| Cardboard Gangsters|                      3|
    |00305e5c73|ea4d08cf70|                Lion|                      4|
    |003ee4c8ac|a902051413|           Limitless|                      3|
    |004e33f215|c590147027|The Zookeeper's Wife|                      6|
    |005f639f10|1fd2f8a29f|  Back to the Future|                      4|
    |005f639f10|445f7f5df7|     Fahrenheit 9/11|                      3|
    |00691f60a9|3db668b28a|The Ballad of Bus...|                      6|
    +----------+----------+--------------------+-----------------------+
    only showing top 10 rows
    


                                                                                    


```python

```
