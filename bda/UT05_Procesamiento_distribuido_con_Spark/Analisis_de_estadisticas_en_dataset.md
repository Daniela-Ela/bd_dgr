# **PR0505. Análisis de estadísticas en dataset**


```python
from pyspark.sql import SparkSession

try:
    spark = ( SparkSession.builder
        .appName("PR0505 - House Prices")
        .master("spark://spark-master:7077")
        .getOrCreate()
    )
    print("SparkSession iniciada correctamente.")
except Exception as e:
    print("Error en la conexión")
    print(e)

from pyspark.sql.types import (StructType, StructField,StringType, IntegerType)

schema = StructType([
    StructField("Index", IntegerType(), True),
    StructField("Title", StringType(), True),
    StructField("Description", StringType(), True),
    StructField("Amount(in rupees)", StringType(), True),
    StructField("Price (in rupees)", IntegerType(), True),
    StructField("location", StringType(), True),
    StructField("Carpet Area", StringType(), True),
    StructField("Status", StringType(), True),
    StructField("Floor", StringType(), True),
    StructField("Transaction", StringType(), True),
    StructField("Furnishing", StringType(), True),
    StructField("facing", StringType(), True),
    StructField("overlooking", StringType(), True),
    StructField("Society", StringType(), True),
    StructField("Bathroom", IntegerType(), True),
    StructField("Balcony", IntegerType(), True),
    StructField("Car Parking", StringType(), True),
    StructField("Ownership", StringType(), True),
    StructField("Super Area", StringType(), True),
    StructField("Dimensions", StringType(), True),
    StructField("Plot Area", StringType(), True),
])

df_precios = (spark.read
    .format("csv")
    .schema(schema)
    .option("header", "true")
    .option("quote", "\"")
    .load("./csv/house_prices.csv")
)

df_precios.printSchema()
df_precios.show(5)

```

    SparkSession iniciada correctamente.
    root
     |-- Index: integer (nullable = true)
     |-- Title: string (nullable = true)
     |-- Description: string (nullable = true)
     |-- Amount(in rupees): string (nullable = true)
     |-- Price (in rupees): integer (nullable = true)
     |-- location: string (nullable = true)
     |-- Carpet Area: string (nullable = true)
     |-- Status: string (nullable = true)
     |-- Floor: string (nullable = true)
     |-- Transaction: string (nullable = true)
     |-- Furnishing: string (nullable = true)
     |-- facing: string (nullable = true)
     |-- overlooking: string (nullable = true)
     |-- Society: string (nullable = true)
     |-- Bathroom: integer (nullable = true)
     |-- Balcony: integer (nullable = true)
     |-- Car Parking: string (nullable = true)
     |-- Ownership: string (nullable = true)
     |-- Super Area: string (nullable = true)
     |-- Dimensions: string (nullable = true)
     |-- Plot Area: string (nullable = true)
    
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+
    |Index|               Title|         Description|Amount(in rupees)|Price (in rupees)|location|Carpet Area|       Status|       Floor|Transaction|    Furnishing|facing|         overlooking|             Society|Bathroom|Balcony|Car Parking|           Ownership|Super Area|Dimensions|Plot Area|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+
    |    0|1 BHK Ready to Oc...|Bhiwandi, Thane h...|          42 Lac |             6000|   thane|   500 sqft|Ready to Move|10 out of 11|     Resale|   Unfurnished|  NULL|                NULL|Srushti Siddhi Ma...|       1|      2|       NULL|                NULL|      NULL|      NULL|     NULL|
    |    1|2 BHK Ready to Oc...|One can find this...|          98 Lac |            13799|   thane|   473 sqft|Ready to Move| 3 out of 22|     Resale|Semi-Furnished|  East|         Garden/Park|         Dosti Vihar|       2|   NULL|     1 Open|            Freehold|      NULL|      NULL|     NULL|
    |    2|2 BHK Ready to Oc...|Up for immediate ...|         1.40 Cr |            17500|   thane|   779 sqft|Ready to Move|10 out of 29|     Resale|   Unfurnished|  East|         Garden/Park|Sunrise by Kalpataru|       2|   NULL|  1 Covered|            Freehold|      NULL|      NULL|     NULL|
    |    3|1 BHK Ready to Oc...|This beautiful 1 ...|          25 Lac |             NULL|   thane|   530 sqft|Ready to Move|  1 out of 3|     Resale|   Unfurnished|  NULL|                NULL|                NULL|       1|      1|       NULL|                NULL|      NULL|      NULL|     NULL|
    |    4|2 BHK Ready to Oc...|This lovely 2 BHK...|         1.60 Cr |            18824|   thane|   635 sqft|Ready to Move|20 out of 42|     Resale|   Unfurnished|  West|Garden/Park, Main...|TenX Habitat Raym...|       2|   NULL|  1 Covered|Co-operative Society|      NULL|      NULL|     NULL|
    +-----+--------------------+--------------------+-----------------+-----------------+--------+-----------+-------------+------------+-----------+--------------+------+--------------------+--------------------+--------+-------+-----------+--------------------+----------+----------+---------+
    only showing top 5 rows
    


## **1. Objetivos de ingeniería de datos (ETL)**

Antes de cualquier análisis, debe ejecutar un pipeline de transformación sobre los datos crudos.

### **1.1. Estandarización monetaria (de INR a USD)**

Las columnas ``Amount(in rupees)`` y ``Price (in rupees)`` vienen en formato de texto con unidades indias (Lac y Cr).
1. **Limpieza**: convierte los textos a valores numéricos puros en rupias (INR). Ten en cuenta que 1 Lac = 100,000 INR y 1 Cr = 10,000,000 INR.
2. **Conversión**: crea una nueva columna ``Amount_USD`` convirtiendo las rupias a dólares. Asume que el valor de conversión es 1 INR = 0.012 USD.


```python
from pyspark.sql import functions as F

df1 = (
    df_precios
    .withColumn(
        "numero",
        F.regexp_extract(F.col("Amount(in rupees)"), r"([0-9.]+)", 1).cast("double")
    )
    .withColumn(
        "medida",
        F.split(F.col("Amount(in rupees)"), " ")[1]
    )
    .withColumn(
        "Amount_INR",
        F.when(F.col("medida") == "Lac", F.col("numero") * 100000)
         .when(F.col("medida") == "Cr", F.col("numero") * 10000000)
         .otherwise(F.col("numero"))
    )
)

df1.select("Amount(in rupees)", "numero", "medida", "Amount_INR").show(10)
```

    +-----------------+------+------+----------+
    |Amount(in rupees)|numero|medida|Amount_INR|
    +-----------------+------+------+----------+
    |          42 Lac |  42.0|   Lac| 4200000.0|
    |          98 Lac |  98.0|   Lac| 9800000.0|
    |         1.40 Cr |   1.4|    Cr|     1.4E7|
    |          25 Lac |  25.0|   Lac| 2500000.0|
    |         1.60 Cr |   1.6|    Cr|     1.6E7|
    |          45 Lac |  45.0|   Lac| 4500000.0|
    |        16.5 Lac |  16.5|   Lac| 1650000.0|
    |          60 Lac |  60.0|   Lac| 6000000.0|
    |          60 Lac |  60.0|   Lac| 6000000.0|
    |         1.60 Cr |   1.6|    Cr|     1.6E7|
    +-----------------+------+------+----------+
    only showing top 10 rows
    



```python
from pyspark.sql import functions as F

df2 = (
    df1
    .withColumn("Amount_USD", F.col("Amount_INR") * 0.012)
)

df2.select("Amount(in rupees)", "Amount_INR", "Amount_USD").show(10)
```

    +-----------------+----------+----------+
    |Amount(in rupees)|Amount_INR|Amount_USD|
    +-----------------+----------+----------+
    |          42 Lac | 4200000.0|   50400.0|
    |          98 Lac | 9800000.0|  117600.0|
    |         1.40 Cr |     1.4E7|  168000.0|
    |          25 Lac | 2500000.0|   30000.0|
    |         1.60 Cr |     1.6E7|  192000.0|
    |          45 Lac | 4500000.0|   54000.0|
    |        16.5 Lac | 1650000.0|   19800.0|
    |          60 Lac | 6000000.0|   72000.0|
    |          60 Lac | 6000000.0|   72000.0|
    |         1.60 Cr |     1.6E7|  192000.0|
    +-----------------+----------+----------+
    only showing top 10 rows
    


### **1.2. Estandarización de superficie**

La columna ``Carpet Area`` está en pies cuadrados (sqft).

1. **Limpieza**: elimina las unidades textuales y extrae el valor numérico.
2. **Conversión**: crea una nueva columna ``Area_m2`` convirtiendo los pies cuadrados a metros cuadrados. El factor de conversión es 1 sqft = 0.0929.


```python
df3 = (
    df2
    .withColumn(
        "Area_m2",
        F.split(F.col("Carpet Area"), " ")[0].cast("double") * 0.0929
    )
)

df3.select("Carpet Area", "Area_m2").show(3)
```

    +-----------+------------------+
    |Carpet Area|           Area_m2|
    +-----------+------------------+
    |   500 sqft|46.449999999999996|
    |   473 sqft|           43.9417|
    |   779 sqft|           72.3691|
    +-----------+------------------+
    only showing top 3 rows
    



```python
print(df3.columns)
```

    ['Index', 'Title', 'Description', 'Amount(in rupees)', 'Price (in rupees)', 'location', 'Carpet Area', 'Status', 'Floor', 'Transaction', 'Furnishing', 'facing', 'overlooking', 'Society', 'Bathroom', 'Balcony', 'Car Parking', 'Ownership', 'Super Area', 'Dimensions', 'Plot Area', 'numero', 'medida', 'Amount_INR', 'Amount_USD', 'Area_m2']


## **2. Objetivos de análisis estadístico**

Utilizando las **nuevas columnas transformadas** (``Amount_USD`` y ``Area_m2``), calcula e interpreta las siguientes métricas de distribución usando PySpark:

### **2.1. Medidas de dispersión (varianza y desviación estándar)**

- Calcula la varianza y la desviación estándar de la columna ``Amount_USD``.
- **Pregunta**: Si la desviación estándar es muy alta en comparación con el precio medio (por ejemplo, si la media es $100k y la desviación es $ 80k), ¿podemos decir que el “precio promedio” es un buen representante del mercado? ¿O los precios son demasiado dispares para confiar en el promedio?
    - Si la desviación estándar es alta respecto a la media, hay mucha variabilidad en los precios,
por lo que el promedio no es un buen resumen del mercado.


```python
stats = df3.select(
    F.mean("Amount_USD").alias("media"),
    F.variance("Amount_USD").alias("varianza"),
    F.stddev("Amount_USD").alias("desv_std")
)
stats.show()
```

    [Stage 24:=======>                                                  (1 + 7) / 8]

    +-----------------+--------------------+-----------------+
    |            media|            varianza|         desv_std|
    +-----------------+--------------------+-----------------+
    |143727.1412747055|2.236814279873181...|472949.7097866941|
    +-----------------+--------------------+-----------------+
    


                                                                                    

### **2.2. Medidas de Forma (Skewness y Kurtosis)**

- Calcule el ``skewness`` (asimetría) y la ``kurtosis`` (curtosis) de ``Amount_USD``.
- **Pregunta**: Suponiendo que has obtenido un valor positivo, ¿qué significa esto para el negocio? ¿Hay más oferta de casas “baratas” con algunas pocas mansiones ultra-caras, o hay muchas casas caras y pocas baratas?
    - Un skewness positivo indica que la distribución de precios está sesgada hacia la derecha. Esto significa que hay muchas viviendas relativamente baratas o de precio medio, mientras que unas pocas propiedades extremadamente caras (mansiones o viviendas de lujo) generan valores muy altos. 
- **Pregunta**: Supón que obtienes una kurtosis superior a 3. ¿Deberíamos preocuparnos por la presencia de datos erróneos o propiedades de lujo extremo que podrían distorsionar nuestros análisis futuros?
    - Sí, deberíamos preocuparnos. Una kurtosis alta indica la presencia de valores extremos (outliers), como propiedades de lujo muy caras o posibles errores en los datos. Estos valores pueden distorsionar la media y afectar negativamente al entrenamiento de modelos de Machine Learning.


```python
stats_forma = df3.select(
    F.skewness("Amount_USD").alias("skewness"),
    F.kurtosis("Amount_USD").alias("kurtosis")
)
stats_forma.show()
```

    [Stage 27:=======>                                                  (1 + 7) / 8]

    +-----------------+-----------------+
    |         skewness|         kurtosis|
    +-----------------+-----------------+
    |270.7690536208719|91491.17725573125|
    +-----------------+-----------------+
    


                                                                                    

## **3. Interpretación para IA**

Redacta un breve informe técnico respondiendo a estas situaciones de modelado:

### **3.1.- Pre-procesamiento para redes neuronales:**

Observando la desviación estándar de ``Amount_USD`` (precio) frente a la de ``Area_m2`` (superficie), notará que tienen escalas muy diferentes (miles de dólares vs. decenas de metros). Realiza los pasos necesarios para homogeneizar las escalas de ambas columnas.


```python
stats_escalado = df3.select(
    F.mean("Amount_USD").alias("mean_price"),
    F.stddev("Amount_USD").alias("std_price"),
    F.mean("Area_m2").alias("mean_area"),
    F.stddev("Area_m2").alias("std_area")
).collect()[0]

mean_price = stats_escalado["mean_price"]
std_price = stats_escalado["std_price"]
mean_area = stats_escalado["mean_area"]
std_area = stats_escalado["std_area"]

print("Media precio:", mean_price)
print("Std precio:", std_price)
print("Media área:", mean_area)
print("Std área:", std_area)
```

    [Stage 30:=======>                                                  (1 + 7) / 8]

    Media precio: 143727.1412747055
    Std precio: 472949.7097866941
    Media área: 111.48601082360713
    Std área: 283.10876647919014


                                                                                    


```python
df_escalado = (
    df3
    .withColumn(
        "Amount_USD_z",
        (F.col("Amount_USD") - F.lit(mean_price)) / F.lit(std_price)
    )
    .withColumn(
        "Area_m2_z",
        (F.col("Area_m2") - F.lit(mean_area)) / F.lit(std_area)
    )
)

df_escalado.select(
    "Amount_USD", "Amount_USD_z",
    "Area_m2", "Area_m2_z"
).show(5, truncate=False)
```

    +----------+--------------------+------------------+--------------------+
    |Amount_USD|Amount_USD_z        |Area_m2           |Area_m2_z           |
    +----------+--------------------+------------------+--------------------+
    |50400.0   |-0.1973299472301128 |46.449999999999996|-0.22972093599364965|
    |117600.0  |-0.05524295867839553|43.9417           |-0.23858078173842762|
    |168000.0  |0.05132228273539241 |72.3691           |-0.13816919663094365|
    |30000.0   |-0.2404634973261698 |49.236999999999995|-0.2198766629438963 |
    |192000.0  |0.10206763578957714 |58.991499999999995|-0.18542170726975965|
    +----------+--------------------+------------------+--------------------+
    only showing top 5 rows
    


### **3.2.- Gestión de outliers (Kurtosis):**

Al calcular la kurtosis de la columna de precios (Amount_USD), puede que obtengas un valor muy alto (mayor a 3, e incluso superior a 10). Si no fuera así supondremos que lo es.

Esto indica una distribución “leptocúrtica” con “colas pesadas”. En el contexto de Big Data, esto significa que unos pocos registros extremos (mansiones de lujo o errores de entrada) están distorsionando la media y la varianza, lo que podría arruinar el entrenamiento de futuros modelos de Machine Learning.

Debes **normalizar** la distribución aplicando una técnica de clipping eliminando los extremos superiores, para ello sigue estos pasos:

#### **Identifica el límite**

En entornos distribuidos, calcular un percentil exacto es computacionalmente muy costoso (requiere ordenar todos los datos). PySpark utiliza algoritmos de aproximación (como Greenwald-Khanna).

Vas a calcular el percentil 99 para eliminar todos los valores que lo superen. En PySpark se hace con el método ``.approxQuantile("Amount_USD", [0.99], 0.01)``. Este método devuelve una lista, por lo que deberás extraer el primer valor. El tercer parámetro (0.01) es la tolerancia de error permitida.


```python
limite_p99 = df3.approxQuantile("Amount_USD", [0.99], 0.01)[0]
print("Percentil 99 de Amount_USD:", limite_p99)
```

    [Stage 34:==================================================>       (7 + 1) / 8]

    Percentil 99 de Amount_USD: 168036000.0


                                                                                    

#### **Aplica el filtro**

Genera un nuevo DataFrame llamado ``df_limpio`` que excluya las propiedades que superen ese precio límite calculado (quédate con el 99% de los datos más “normales”).


```python
df_limpio = df3.filter(F.col("Amount_USD") <= limite_p99)
```

#### **Verificación**

Vuelve a calcular la kurtosis, la media y la stddev sobre este nuevo DataFrame ``df_limpio``.


```python
stats_antes = df3.select(
    F.mean("Amount_USD").alias("media_antes"),
    F.stddev("Amount_USD").alias("std_antes"),
    F.kurtosis("Amount_USD").alias("kurtosis_antes")
)

stats_antes.show(truncate=False)
```

    +-----------------+-----------------+-----------------+
    |media_antes      |std_antes        |kurtosis_antes   |
    +-----------------+-----------------+-----------------+
    |143727.1412747055|472949.7097866941|91491.17725573125|
    +-----------------+-----------------+-----------------+
    



```python
stats_despues = df_limpio.select(
    F.mean("Amount_USD").alias("media_despues"),
    F.stddev("Amount_USD").alias("std_despues"),
    F.kurtosis("Amount_USD").alias("kurtosis_despues")
)

stats_despues.show(truncate=False)
```

    [Stage 39:>                                                         (0 + 8) / 8]

    +-----------------+-----------------+-----------------+
    |media_despues    |std_despues      |kurtosis_despues |
    +-----------------+-----------------+-----------------+
    |143727.1412747055|472949.7097866941|91491.17725573125|
    +-----------------+-----------------+-----------------+
    


                                                                                    

**Pregunta**: comparando los resultados antes y después del filtro: ¿Cuánto ha bajado la curtosis? ¿Ha cambiado drásticamente el precio medio al eliminar solo el 1% de los datos? Reflexiona sobre la sensibilidad de la media aritmética frente a los outliers en grandes volúmenes de datos.
- Al comparar las métricas antes y después del filtrado, se observa que la curtosis no ha cambiado y las estadísticas permanecen iguales. Esto ocurre porque el percentil 99 coincide con el valor máximo del dataset, por lo que el filtro no eliminó ningún registro.
- Aun así, el valor extremadamente alto de la curtosis indica la presencia de outliers muy extremos en los precios de las propiedades. Esto demuestra que la media aritmética es muy sensible a estos valores extremos, ya que unos pocos registros pueden distorsionar significativamente métricas como la desviación estándar y la curtosis en grandes volúmenes de datos.

## **4. Análisis de Segmentos (Grouping & Aggregation)**

Algo que nos puede ocurrir al realizar el análisis estadístico sobre el dataset completo es que las métricas globales calculadas están “sucias” porque mezclan tipos de propiedades muy diferentes (no es justo comparar un estudio de 1 habitación con un ático de 4 habitaciones).

### **4.1.- Ingeniería de variable (Extracción de BHK - Bedroom-Hall-Kitchen):**
- La columna ``Title`` contiene información como “1 BHK Ready to Occupy…” o “2 BHK…“.
- Crea una nueva columna llamada ``Num_Bedrooms`` extrayendo el número antes de “BHK”


```python
df4 = (
    df3
    .withColumn("Num_Bedrooms",F.split(F.col("Title"), " " )[0].cast("int"))
)

df4.select("Num_bedrooms", "Title").show(4)
```

    +------------+--------------------+
    |Num_bedrooms|               Title|
    +------------+--------------------+
    |           1|1 BHK Ready to Oc...|
    |           2|2 BHK Ready to Oc...|
    |           2|2 BHK Ready to Oc...|
    |           1|1 BHK Ready to Oc...|
    +------------+--------------------+
    only showing top 4 rows
    


### **4.2.- Cálculo de estadísticas por grupo:**
Agrupa los datos por ``Num_Bedrooms`` (ej. 1 BHK, 2 BHK, 3 BHK).
Para cada grupo, calcula simultáneamente: ``Mean``, ``StdDev`` y ``Skewness`` del precio (``Amount_USD``).


```python
agrup = (df4.groupBy("Num_Bedrooms").agg(
    F.mean("Amount_USD").alias("mean_price"),
    F.stddev("Amount_USD").alias("std_price"),
    F.skewness("Amount_USD").alias("skew_price"),
    F.kurtosis("Amount_USD").alias("kurt_price") 
))

agrup.show()
```

    [Stage 59:=======>                                                  (1 + 7) / 8]

    +------------+------------------+------------------+-------------------+-------------------+
    |Num_Bedrooms|        mean_price|         std_price|         skew_price|         kurt_price|
    +------------+------------------+------------------+-------------------+-------------------+
    |        NULL|172576.50429799428|  685004.728180962|  9.416998973680867| 110.48658564580589|
    |           1| 42374.56647398844| 32281.36564982392|   4.06051551542482|  33.01952265661245|
    |           6| 844643.4782608695| 910736.4390346808| 1.8175914038274064| 3.2396218028759574|
    |           3|165416.28207898515| 647176.2825118777| 232.51788101696198|  58545.98406546377|
    |           5| 549332.2914837577| 472230.8397278678|  6.277443623698031|  61.99103175451414|
    |           9|436285.71428571426| 190736.9167952849|-0.2051309353148022|-1.4406103915346804|
    |           4| 367778.9972451791| 294358.7242137188|  4.191869405681075|  43.70870422649105|
    |           8|         2507820.0|1946900.5176433644|0.06164867132208699| -1.799848731210454|
    |           7| 682742.8571428572| 725893.0310806328| 1.8506352685940017|  2.679962529186576|
    |          10| 796254.5454545454|1363400.5166227834| 2.6012315773520585|  5.207930779470404|
    |           2| 74568.32623871956|212636.25068488342|  189.3063979141958|  39407.92856080018|
    +------------+------------------+------------------+-------------------+-------------------+
    


                                                                                    

### **4.3. Preguntas de análisis para el modelo:**

#### **A. Análisis de variabilidad (Desviación Estándar):**
Observa cómo cambia la desviación estándar de los precios a medida que aumentan las habitaciones. ¿La variabilidad se mantiene constante o se dispara en las propiedades más grandes?

**Pregunta:** Si la desviación es mucho mayor en los pisos de 3 BHK que en los de 1 BHK, ¿qué nos indica esto sobre la homogeneidad del producto?

**Pista:** Un mercado con baja desviación sugiere que los inmuebles son muy parecidos entre sí (commodities). Una alta desviación sugiere que dentro de esa categoría conviven pisos “estándar” con propiedades de “ultra-lujo”, haciendo que el mercado sea mucho más heterogéneo.

- La desviación estándar aumenta considerablemente a medida que crece el número de habitaciones. Esto indica que los apartamentos más grandes presentan una mayor variabilidad en sus precios. En los pisos de 3 BHK o más conviven propiedades estándar con viviendas de lujo, lo que hace que el mercado sea mucho más heterogéneo.

### **B. Confiabilidad del precio promedio:**
**Pregunta**: Basándote en lo anterior, ¿en qué segmento (1 BHK o 3 BHK) dirías que el “Precio Promedio” es un indicador más fiable del valor real de una propiedad? Es decir, si tuvieras que tasar una propiedad “a ciegas” usando solo el promedio del mercado, ¿en qué tipo de apartamento tendrías más riesgo de equivocarte drásticamente por exceso o por defecto?
- El precio promedio es más fiable en el segmento de 1 BHK, ya que los precios son más homogéneos y la desviación estándar es relativamente baja. En cambio, en los apartamentos de 3 BHK o más existe una gran variabilidad en los precios, lo que hace que el promedio sea menos representativo del valor real de una propiedad.

#### **C. Detección de anomalías de mercado (Curtosis):**
Compara la curtosis entre los apartamentos pequeños y los grandes.

**Pregunta:** ¿Qué segmento tiene una curtosis más alta (colas más pesadas)?

**Pregunta:** Si el segmento de 3 BHK tiene una curtosis muy elevada, significa que existen propiedades con precios desorbitados que rompen la norma. ¿Consideras que estas “mansiones” representan la realidad del barrio, o son excepciones que deberían analizarse en un estudio de mercado aparte para no distorsionar la visión general?
- El segmento de 3 BHK presenta una curtosis extremadamente alta, lo que indica la presencia de valores extremos en los precios. Esto sugiere que existen propiedades de lujo con precios muy elevados que generan colas pesadas en la distribución. Estas propiedades no representan el comportamiento típico del mercado y deberían analizarse por separado para evitar que distorsionen el análisis general.


```python

```
