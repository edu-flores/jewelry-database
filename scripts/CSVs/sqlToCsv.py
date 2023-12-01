import pandas as pd
import mysql.connector

# Los datos de ingreso a la base de datos deberan de ser los de la base de datos en el cluster para que funcione PySpark
database_config = {
    'host': 'localhost',
    'user': 'user',
    'password': '666',
    'database': 'jewelry'
}
conn = mysql.connector.connect(**database_config)

# La query del primer analisis
sql_query = "SELECT name, ((total_distance / 25) * 2.68) AS total_CO2 FROM trucks;"
df = pd.read_sql_query(sql_query, conn)

# Lo guardamos en un archivo csv 
df.to_csv('datosCO2.csv', index=False)

#Repetimos el proceso para cada analisis

sql_query = "SELECT routes.route_id, name, duration FROM long_stops, routes WHERE routes.route_id = long_stops.route_id;"
df = pd.read_sql_query(sql_query, conn)
df.to_csv('datosRutasLargas.csv', index=False)

sql_query = "SELECT routes.route_id, name, duration FROM short_stops, routes WHERE routes.route_id = short_stops.route_id;"
df = pd.read_sql_query(sql_query, conn)
df.to_csv('datosRutasCortas.csv', index=False)

conn.close()