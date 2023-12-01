from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Configuración de Apache Spark
spark = SparkSession.builder.appName("AnalisisCO2").getOrCreate()

# Hacemos la lectura del archivo CSV
ruta_archivo_hadoop = "hdfs:///jpzp20012/datosCO2.csv"
df = spark.read.csv(ruta_archivo_hadoop, header=True, inferSchema=True)

# Desplegamos el resultado
df.show()