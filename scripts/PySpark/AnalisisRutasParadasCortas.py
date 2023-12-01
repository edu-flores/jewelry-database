from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Configuración de Apache Spark
spark = SparkSession.builder.appName("AnalisisRutasParadasCortass").getOrCreate()

# Hacemos la lectura del archivo CSV
ruta_archivo_hadoop = "hdfs:///jpzp20012/datosRutasCortas.csv"
df = spark.read.csv(ruta_archivo_hadoop, header=True, inferSchema=True)

# Agrupamos por nombre y sumamos la duracion de las paradas por cada camion
grouped_df = df.groupBy("name").agg(F.sum("duration").alias("Tiempo total en paradas cortas"))

# Sacamos las rutas con mayor y menor tiempo gastado
max_duration_route = grouped_df.orderBy(F.desc("Tiempo total en paradas cortas")).first()
min_duration_route = grouped_df.orderBy("Tiempo total en paradas cortas").first()

# Desplegamos el resultado
grouped_df.show()
print("La ruta más eficiente es la ruta:", min_duration_route["name"])
print("La ruta menos eficiente es la ruta:", max_duration_route["name"])