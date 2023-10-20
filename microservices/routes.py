################### Correr microservicio en puerto 5001
# Flask
from flask import Flask, request, url_for, jsonify
from flask_mysqldb import MySQL

# Misc
from dotenv import load_dotenv
import os
load_dotenv()

# Microservice app
routes = Flask(__name__)

routes.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
routes.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
routes.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
routes.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
routes.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(routes)

@routes.route("/retrieve_routes", methods=["POST"])
def retrieve_routes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT r.route_id, r.name, r.distance, r.active, r.average_speed, r.time, t.name FROM routes AS r LEFT JOIN trucks AS t ON r.truck_id = t.truck_id")
    routes = cursor.fetchall()
    print(routes)
    cursor.close()
    if routes:
        routesJSON = [{"id": route[0], "name": route[1], "distance": route[2], "active": route[3], "average_speed": route[4], "time": route[5], "truck_name": route[6], "error": False} for route in routes]
        return jsonify(routesJSON), 200
    else:
        return jsonify({"error": False}),401
    
@routes.route("/add_route", methods=["POST"])
def add_route():
    data = request.get_json()
    name = data["name"]
    distance = data["distance"]
    activo = data["activo"]
    average_speed = data["average_speed"]
    time = data["time"]
    truck_id = data["truck_id"]

    cursor = mysql.connection.cursor()
    if truck_id == -1:
        cursor.execute("INSERT INTO routes (name, distance, active, average_speed, time) VALUES (%s,%s,%s,%s,%s)",(name,distance,activo,average_speed,time))
    else:
        cursor.execute("INSERT INTO routes (name, distance, active, average_speed, time, truck_id) VALUES (%s,%s,%s,%s,%s,%s)",(name,distance,activo,average_speed,time,truck_id))
    mysql.connection.commit()
    cursor.close()

    return "Se agregó correctamente la ruta"

@routes.route("/edit_route", methods=["POST"])
def edit_route():
    data = request.get_json()
    id = data["id"]
    name = data["name"]
    distance = data["distance"]
    activo = data["activo"]
    average_speed = data["average_speed"]
    time = data["time"]
    truck_id = data["truck_id"]

    cursor = mysql.connection.cursor()
    if truck_id == -1:
        cursor.execute("""UPDATE routes SET 
            name=%s, distance=%s, active=%s, average_speed=%s, time=%s
            WHERE route_id = %s """, (name, distance, activo, average_speed, time, id))
    else:
        cursor.execute("""UPDATE routes SET 
            name=%s, distance=%s, active=%s, average_speed=%s, time=%s, truck_id=%s
            WHERE route_id = %s """, (name, distance, activo, average_speed, time, truck_id, id))
    mysql.connection.commit()
    cursor.close()

    return "Se actualizó correctamente la ruta"

@routes.route("/retrieve_route", methods=["POST"])
def retrieve_route():
    data = request.get_json()
    id = data["id"]
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM routes WHERE route_id = %s",(id,))
    route = cursor.fetchone()
    cursor.close()

    if route:
        return jsonify({"route_id": route[0], "name": route[1], "distance": route[2], "active": route[3], "average_speed": route[4], "time": route[5], "truck_id": route[6]}), 200
    else:
        return jsonify({"error", False}), 401

@routes.route("/retrieve_trucks", methods=["POST"])
def retrieve_trucks():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT truck_id, name FROM trucks")
    trucks = cursor.fetchall()
    cursor.close()

    if trucks:
        trucksJSON = [{"id": truck[0], "name": truck[1]} for truck in trucks]
        return jsonify(trucksJSON), 200
    else:
        return jsonify({"error", False}), 401
    
@routes.route("/delete_route", methods=["POST"])
def delete_route():
    data = request.get_json()
    id = data["id"]

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM routes WHERE route_id = %s",(id,))
    mysql.connection.commit()
    cursor.close()

    return "Eliminado Exsitosamente"
