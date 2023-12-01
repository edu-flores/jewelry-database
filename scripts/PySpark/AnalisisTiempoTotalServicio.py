from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Configuración de Apache Spark
spark = SparkSession.builder.appName("AnalisisTiempoServicio").getOrCreate()

# Hacemos la lectura del archivo CSV
ruta_archivo_hadoop = "hdfs:///jpzp20012/datosGPS3.csv"
df = spark.read.csv(ruta_archivo_hadoop, header=True, inferSchema=True)

# Transformamos la columna datetime a tipo timestamp
df = df.withColumn('datetime', F.to_timestamp('datetime'))


window_spec = Window.partitionBy('truck_name').orderBy('datetime')
df = df.withColumn('time_on_road', F.col('datetime').cast('long') - F.lag('datetime').over(window_spec).cast('bigint'))

# Rellenamos los valores que quedaron en nulo
df = df.fillna(0, subset=['time_on_road'])

# Agrupamos por nombre de camion
result_df = df.groupBy("truck_name").agg((F.sum("time_on_road") / 60).alias("Total Time on Service (min)"))

# Desplegamos el resultado
result_df.show()