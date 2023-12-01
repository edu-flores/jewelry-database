from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Configuración de Apache Spark
spark = SparkSession.builder.appName("AnalisisRutasParadasLargas").getOrCreate()

# Hacemos la lectura del archivo CSV
ruta_archivo_hadoop = "hdfs:///jpzp20012/datosRutasLargas.csv"
df = spark.read.csv(ruta_archivo_hadoop, header=True, inferSchema=True)

# Agrupamos por nombre de ruta y sumamos las duraciones de las paradas
grouped_df = df.groupBy("name").agg(F.sum("duration").alias("Tiempo total en paradas largas"))

# Sacamos las rutas con mayor y menor tiempo gastado en paradas largas
max_duration_route = grouped_df.orderBy(F.desc("Tiempo total en paradas largas")).first()
min_duration_route = grouped_df.orderBy("Tiempo total en paradas largas").first()

# Desplegamos el resultado
grouped_df.show()
print("La ruta más eficiente es la ruta:", min_duration_route["name"])
print("La ruta menos eficiente es la ruta:", max_duration_route["name"])