# **PR0503. Limpieza de datos sobre dataset de lugares famosos**

## **Dataset 2**

Seguimos trabajando con dataframes en PySpark. En esta ocasión el objetivo es transformar datos crudos de destinos turísticos para limpieza de texto, cálculos matemáticos avanzados y gestión de fechas.

Supón que en la empresa en la que estás trabajando está preparando un catálogo turístico y el departamento de marketing necesita un dataset enriquecido con códigos cortos para la app móvil, precios ajustados psicológicamente y fechas límite para ofertas promocionales.

Trabajarás sobre el archivo el mismo dataset de la práctica anterior.


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
    26/02/01 17:11:04 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


    SparkSession iniciada correctamente.



```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, IntegerType 

schema = StructType([
    StructField("Place_Name", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("City", StringType(), True),
    StructField("Annual_Visitors_Millions", DoubleType(), True),
    StructField("Type", StringType(), True),
    StructField("UNESCO_World_Heritage", StringType(), True), 
    StructField("Year_Built", IntegerType(), True),
    StructField("Entry_Fee_USD", DoubleType(), True),
    StructField("Best_Visit_Month", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Tourism_Revenue_Million_USD", IntegerType(), True),
    StructField("Average_Visit_Duration_Hours", DoubleType(), True),
    StructField("Famous_For", StringType(), True)
])

df_lugares = (spark.read
    .format("csv")
    .option("header", "true")
    .schema(schema)
    .load("./world_famous_places_2024.csv")
)

df_lugares.show(1)

```

    +------------+-------+-----+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |  Place_Name|Country| City|Annual_Visitors_Millions|          Type|UNESCO_World_Heritage|Year_Built|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|
    +------------+-------+-----+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |Eiffel Tower| France|Paris|                     7.0|Monument/Tower|                   No|      1889|         35.0|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|
    +------------+-------+-----+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    only showing top 1 row
    


### **Ejercicio 1: Generación de códigos SKUs**

La App móvil no puede mostrar nombres largos. Necesitamos un **SKU (Stock Keeping Unit)** para cada lugar.

Para ello tienes que crear una columna ``SKU_Lugar`` en un nuevo DataFrame ``df_feat``. El formato debe ser ``PAIS(3)-CIUDAD(3)-TIPO``. Debes tener en cuenta:
- **País**: extrae los 3 primeros caracteres del ``Country`` y conviértelos a mayúsculas (``upper``, ``substring``).
- **Ciudad**: extrae los 3 primeros caracteres de ``City``. Si la ciudad tiene menos de 3 letras (raro, pero posible), rellena con ‘X’ a la derecha (``rpad``).
- **Tipo**: la columna ``Type`` a veces tiene barras (ej: “Monument/Tower”). Queremos solo la **primera parte** antes de la barra. Usa ``split`` para dividir el texto y extrae el primer elemento (índice 0).
- **Unión**: concatena todo con guiones bajos (``concat_ws``).


```python
from pyspark.sql.functions import upper, substring, col, concat_ws, rpad, split

df_feat = (
    df_lugares
    .withColumn(
        "SKU_Lugar",
        concat_ws(
            "_",
            upper(substring(col("Country"), 1, 3)),            
            rpad(upper(substring(col("City"), 1, 3)), 3, "X"),  
            upper(split(col("Type"), "/")[0])                              
        )
    )
)

df_feat.select("SKU_Lugar").show(4)
```

    +--------------------+
    |           SKU_Lugar|
    +--------------------+
    |    FRA_PAR_MONUMENT|
    |UNI_NEW_URBAN LAN...|
    |      FRA_PAR_MUSEUM|
    |CHI_BEI_HISTORIC ...|
    +--------------------+
    only showing top 4 rows
    


### **Ejercicio 2: Ajuste de precios y tiempos**

Necesitamos normalizar las métricas para el algoritmo de recomendación.

Añade las siguientes columnas numéricas:
- **``Duracion_Techo``**: la ``Average_Visit_Duration_Hours`` tiene decimales (2.5 horas). Redondea siempre hacia arriba (``ceil``) para reservar bloques completos en la agenda del turista.
- **``Log_Ingresos``**: los ingresos (``Tourism_Revenue_Million_USD``) varían demasiado (de 45 a 180). Aplica una transformación logarítmica (``log10``) para suavizar la escala.
- **``Mejor_Oferta``**: compara el ``Entry_Fee_USD`` actual contra un “Precio de Competencia” simulado (que es siempre 20 USD). Usa la función ``least`` para quedarte con el precio más bajo de los dos (fila a fila).


```python
from pyspark.sql import functions as F

df_feat = (
    df_feat
    .withColumn("Duracion_Techo", F.ceil(F.col("Average_Visit_Duration_Hours")))
    .withColumn("Log_Ingresos", F.log10(F.col("Tourism_Revenue_Million_USD") + F.lit(1)))
    .withColumn("Mejor_Oferta", F.least(F.col("Entry_Fee_USD"), F.lit(20.0)))
)

df_feat.select("Duracion_Techo","Log_Ingresos","Mejor_Oferta").show(3)
```

    +--------------+------------------+------------+
    |Duracion_Techo|      Log_Ingresos|Mejor_Oferta|
    +--------------+------------------+------------+
    |             3|1.9822712330395684|        20.0|
    |             2|1.8512583487190752|         0.0|
    |             4|  2.08278537031645|        20.0|
    +--------------+------------------+------------+
    only showing top 3 rows
    


### **Ejercicio 3: Limpieza de texto**

La columna ``Famous_For`` es demasiado larga para las notificaciones push.

Haz lo siguiente:
- Crea **``Desc_Corta``**: extrae solo los primeros 15 caracteres de ``Famous_For`` (``substring``).
- Crea **``Ciudad_Limpia``**: reemplaza la cadena “New York City” por “NYC” usando ``regexp_replace`` en la columna ``City``.


```python
from pyspark.sql import functions as F

df_feat = (
    df_feat
    .withColumn(
        "Desc_Corta",
        F.substring(F.col("Famous_For"), 1, 15)
    )
    .withColumn(
        "Ciudad_Limpia",
        F.regexp_replace(F.col("City"), "New York City", "NYC")
    )
)

df_feat.select("Famous_For", "Desc_Corta", "City", "Ciudad_Limpia").show(4)
```

    +--------------------+---------------+----------------+----------------+
    |          Famous_For|     Desc_Corta|            City|   Ciudad_Limpia|
    +--------------------+---------------+----------------+----------------+
    |Iconic iron latti...|Iconic iron lat|           Paris|           Paris|
    |Bright lights, Br...|Bright lights, |   New York City|             NYC|
    |World's most visi...|World's most vi|           Paris|           Paris|
    |Ancient defensive...|Ancient defensi|Beijing/Multiple|Beijing/Multiple|
    +--------------------+---------------+----------------+----------------+
    only showing top 4 rows
    


### **Ejercicio 4: Gestión de fechas de campaña**

Vamos a simular que lanzamos una campaña hoy.
- Crea una columna ``Inicio_Campana`` usando ``to_date`` con la fecha “2024-06-01”.
- Crea ``Fin_Campana``: Suma 90 días a la fecha de inicio (``date_add``).
- Crea ``Dias_Hasta_Fin``: Calcula la diferencia en días entre el fin de la campaña y la fecha de construcción del monumento.

**Nota**:
- Como ``Year_Built`` es un número (ej. 1889), primero deberás crear una fecha ficticia de construcción. Usa ``concat`` para unir el año con “-01-01” (ej: “1889-01-01”) y conviértelo a fecha con ``to_date``.
- Si el año tiene texto (como “220 BC”), ``to_date`` devolverá null, lo cual es correcto para este ejercicio.


```python
from pyspark.sql import functions as F

df_feat = (
    df_feat
    .withColumn(
        "Inicio_Campana",
        F.to_date(F.lit("2024-06-01"))
    )
    .withColumn(
        "Fin_Campana",
        F.date_add(F.col("Inicio_Campana"), 90)
    )
    .withColumn(
        "Fecha_Construccion",
        F.to_date(
            F.concat(F.col("Year_Built"), F.lit("-01-01"))
        )
    )
    .withColumn(
        "Dias_Hasta_Fin",
        F.datediff(F.col("Fin_Campana"), F.col("Fecha_Construccion"))
    )
)
df_feat.select("Year_Built","Fecha_Construccion","Inicio_Campana","Fin_Campana","Dias_Hasta_Fin").show(6)
```

    +----------+------------------+--------------+-----------+--------------+
    |Year_Built|Fecha_Construccion|Inicio_Campana|Fin_Campana|Dias_Hasta_Fin|
    +----------+------------------+--------------+-----------+--------------+
    |      1889|        1889-01-01|    2024-06-01| 2024-08-30|         49549|
    |      1904|        1904-01-01|    2024-06-01| 2024-08-30|         44072|
    |      1793|        1793-01-01|    2024-06-01| 2024-08-30|         84612|
    |      NULL|              NULL|    2024-06-01| 2024-08-30|          NULL|
    |      1653|        1653-01-01|    2024-06-01| 2024-08-30|        135746|
    |        80|              NULL|    2024-06-01| 2024-08-30|          NULL|
    +----------+------------------+--------------+-----------+--------------+
    only showing top 6 rows
    



```python
spark.stop()
```


```python

```
