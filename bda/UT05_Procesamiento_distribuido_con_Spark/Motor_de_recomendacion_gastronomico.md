# **PR0505. Creación de un motor de recomendación gastronómica**

## **Contexto**

En esta práctica trabajarás con el dataset Restaurant Recommendations que contiene una relación de usuarios y restaurantes con sus valoraciones.

Tu objetivo será construir un motor de recomendación inteligente que sugiera a cada usuario restaurantes que probablemente le encantarán, basándose en el historial de valoraciones de toda la comunidad.

## **El conjunto de datos**

Para esta primera versión del motor, trabajaremos exclusivamente con el archivo **``ratings.csv``**. Este fichero contiene el historial de valoraciones que los usuarios han dejado en diferentes lugares

Su estructura es muy sencilla:
- ``user_id``: identificador único del usuario.
- ``venue_id``: identificador único del restaurante/local.
- ``rating``: la nota que el usuario le dio a ese local (del 1 al 5).

## **Tareas a realizar**

Deberás crear un script o Notebook en PySpark que ejecute el flujo completo de aprendizaje automático. Sigue estos pasos:


```python
!pip install numpy
```

    Collecting numpy
      Downloading numpy-2.2.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.8 MB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m16.8/16.8 MB[0m [31m16.0 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hInstalling collected packages: numpy
    Successfully installed numpy-2.2.6
    [33mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv[0m[33m
    [0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.0.1[0m[39;49m -> [0m[32;49m26.0.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m



```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType
from pyspark.sql import functions as F

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
```

### **Fase 1: Preparación de datos**

1. **Inicializa PySpark**: crea la sesión de Spark con un nombre descriptivo para la aplicación.
2. **Carga de datos**: lee el archivo ratings.csv y guárdalo en un DataFrame. Asegúrese de que las columnas tengan el tipo de dato correcto (enteros para los IDs y numérico/double para el rating).
3. **División de la muestra**: separa el DataFrame en dos bloques usando una semilla para que tus resultados sean reproducibles:
    - **80**% para entrenamiento (tren).
    - **20**% para evaluación (test).


```python
# 1. Inicializar PySpark
spark = (
    SparkSession.builder
    .appName("RestaurantRecommendationALS")
    .getOrCreate()
)

# 2. Definir esquema 
schema = StructType([
    StructField("user_id", IntegerType(), False),
    StructField("venue_id", IntegerType(), False),
    StructField("rating", DoubleType(), False)
])

# 3. Cargar ratings.csv
ratings_path = "./csv/ratings.csv"

ratings_df = (
    spark.read
    .option("header", True)
    .schema(schema)
    .csv(ratings_path)
)

print("=== Esquema del dataset ===")
ratings_df.printSchema()

print("=== Primeras filas ===")
ratings_df.show(5, truncate=False)

print(f"Número total de filas originales: {ratings_df.count()}")

# 4. Limpiar posibles duplicados usuario-restaurante
ratings_clean = (
    ratings_df
    .groupBy("user_id", "venue_id")
    .agg(F.avg("rating").alias("rating"))
)

print(f"Número total de filas tras agrupar duplicados: {ratings_clean.count()}")

# 5. División train/test (80/20) con seed
train, test = ratings_clean.randomSplit([0.8, 0.2], seed=42)

print(f"Train: {train.count()} filas")
print(f"Test: {test.count()} filas")
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/03/09 12:03:07 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
    26/03/09 12:03:08 WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.


    === Esquema del dataset ===
    root
     |-- user_id: integer (nullable = true)
     |-- venue_id: integer (nullable = true)
     |-- rating: double (nullable = true)
    
    === Primeras filas ===


                                                                                    

    +-------+--------+------+
    |user_id|venue_id|rating|
    +-------+--------+------+
    |1      |1       |5.0   |
    |1      |51      |4.0   |
    |1      |51      |2.0   |
    |1      |51      |5.0   |
    |1      |52      |5.0   |
    +-------+--------+------+
    only showing top 5 rows
    
    Número total de filas originales: 2809580


    26/03/09 12:03:21 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors
                                                                                    

    Número total de filas tras agrupar duplicados: 2436723


                                                                                    

    Train: 1949755 filas


    [Stage 18:>                                                         (0 + 8) / 8]

    Test: 486968 filas


                                                                                    

### **Fase 2: Construcción y búsqueda del modelo óptimo**

No sabemos qué configuración matemática es la mejor para nuestros usuarios, así que vamos a automatizar la búsqueda.
1. **Instancia el modelo ALS**: configure las columnas de entrada (``userCol``, ``itemCol``, ``ratingCol``). No olvides configurar la estrategia adecuada para el arranque en frío (``coldStartStrategy``) para evitar errores en la evaluación.
2. **Crea la cuadrícula de hiperparámetros (ParamGrid)**: configura al menos las siguientes combinaciones para que el sistema las pruebe:
- ``rank``(Factores latentes): Prueba con 5, 10 y 15.
- ``regParam``(Regularización): Prueba con 0.01 y 0.1.
- ``maxIter``(Iteraciones): Fíjalo en 10 para no sobrecargar el sistema.
3. **Configura el evaluador**: utiliza un ``RegressionEvaluator`` que mida el error usando la métrica RMSE .
4. **Validación cruzada (CrossValidator)**: ensambla el modelo, la cuadrícula y el evaluador usando ``numFolds=3`` para asegurar un entrenamiento robusto. Ejecuta el entrenamiento sobre tu **80% de datos**. (Diez en cuenta que este paso puede tardar unos minutos).


```python
spark.sparkContext.setLogLevel("ERROR")

als = ALS(
    userCol="user_id",
    itemCol="venue_id",
    ratingCol="rating",
    coldStartStrategy="drop"
)

paramGrid = (
    ParamGridBuilder()
    .addGrid(als.rank, [5, 10])
    .addGrid(als.regParam, [0.01])
    .addGrid(als.maxIter, [5])
    .build()
)

evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)

crossval = CrossValidator(
    estimator=als,
    estimatorParamMaps=paramGrid,
    evaluator=evaluator,
    numFolds=2,
    seed=42
)

cv_model = crossval.fit(train)
```

                                                                                    

### **Fase 3: evaluación y resultados**

A partir del objeto de validación cruzada, extrae el mejor modelo y muestra por pantalla mediante código cuáles han sido los hiperparámetros ganadores (``rank`` y regParam).


```python
# 11. Mejor modelo
best_model = cv_model.bestModel

# 12. Hiperparámetros ganadores
print("=== Mejores hiperparámetros ===")
print(f"rank ganador: {best_model.rank}")
print(f"regParam ganador: {best_model._java_obj.parent().getRegParam()}")
print(f"maxIter usado: {best_model._java_obj.parent().getMaxIter()}")

# 13. Evaluación sobre test
predictions = best_model.transform(test)
rmse = evaluator.evaluate(predictions)

print(f"RMSE en test: {rmse:.4f}")
```

    === Mejores hiperparámetros ===
    rank ganador: 10
    regParam ganador: 0.01
    maxIter usado: 5


    [Stage 3221:>                                                       (0 + 8) / 8]

    RMSE en test: 4.0935


                                                                                    

### **Fase 4: Puesta en Producción**

1. Selecciona a un usuario cualquiera de tu dataset (por ejemplo, el ``user_id = 1``).
2. Utiliza la función específica de Spark para subconjuntos de usuarios y obtén sus **15 mejores restaurantes recomendados**.
3. Limpia la salida para que se muestre en un formato de tabla legible (Usuario, Restaurante, Nota Predicha).


```python
# 14. Usuario objetivo
target_user_id = 1

# 15. Crear DataFrame con el usuario
user_subset = spark.createDataFrame([(target_user_id,)], ["user_id"])

# 16. Obtener 15 recomendaciones
recommendations = best_model.recommendForUserSubset(user_subset, 15)

# 17. Limpiar formato de salida
recommendations_clean = (
    recommendations
    .select("user_id", F.explode("recommendations").alias("rec"))
    .select(
        F.col("user_id").alias("Usuario"),
        F.col("rec.venue_id").alias("Restaurante"),
        F.round(F.col("rec.rating"), 3).alias("Nota_Predicha")
    )
    .orderBy(F.col("Nota_Predicha").desc())
)

recommendations_clean.show(15, truncate=False)
```

    [Stage 3357:===================================================>  (76 + 4) / 80]

    +-------+-----------+-------------+
    |Usuario|Restaurante|Nota_Predicha|
    +-------+-----------+-------------+
    |1      |650037     |54.334       |
    |1      |429129     |48.746       |
    |1      |565831     |48.637       |
    |1      |62942      |47.257       |
    |1      |299480     |46.998       |
    |1      |138268     |43.534       |
    |1      |547391     |43.081       |
    |1      |658684     |42.737       |
    |1      |231324     |42.71        |
    |1      |341555     |41.309       |
    |1      |7589       |41.263       |
    |1      |417328     |41.192       |
    |1      |270046     |40.912       |
    |1      |18289      |40.879       |
    |1      |564431     |40.618       |
    +-------+-----------+-------------+
    


                                                                                    


```python

```
