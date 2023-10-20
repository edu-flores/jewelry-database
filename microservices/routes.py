################### PORT 5003 ###################

# Flask
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

# XML generator
import xml.etree.ElementTree as ET

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

"""CRUD"""

@routes.route("/retrieve-routes", methods=["POST"])
def retrieve_routes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT r.route_id, r.name, r.distance, r.active, r.average_speed, r.time, t.name FROM routes AS r LEFT JOIN trucks AS t ON r.truck_id = t.truck_id")
    routes = cursor.fetchall()

    cursor.close()
    if routes:
        routesJSON = [{"id": route[0], "name": route[1], "distance": route[2], "active": route[3], "average_speed": route[4], "time": route[5], "truck_name": route[6], "error": False} for route in routes]
        return jsonify(routesJSON), 200
    else:
        return jsonify({"error": False}), 401

@routes.route("/add-route", methods=["POST"])
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
        cursor.execute("INSERT INTO routes (name, distance, active, average_speed, time) VALUES (%s,%s,%s,%s,%s)", (name, distance, activo, average_speed, time))
    else:
        cursor.execute("INSERT INTO routes (name, distance, active, average_speed, time, truck_id) VALUES (%s,%s,%s,%s,%s,%s)", (name, distance, activo, average_speed, time, truck_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Se agregó correctamente la ruta", "error": False}), 200

@routes.route("/edit-route", methods=["POST"])
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

    return jsonify({"message": "Se actualizó correctamente la ruta", "error": False}), 200

@routes.route("/retrieve-route", methods=["POST"])
def retrieve_route():
    data = request.get_json()
    id = data["id"]
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM routes WHERE route_id = %s", (id,))
    route = cursor.fetchone()
    cursor.close()

    if route:
        return jsonify({"route_id": route[0], "name": route[1], "distance": route[2], "active": route[3], "average_speed": route[4], "time": route[5], "truck_id": route[6]}), 200
    else:
        return jsonify({"error", False}), 401

@routes.route("/retrieve-trucks", methods=["POST"])
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

@routes.route("/delete-route", methods=["POST"])
def delete_route():
    data = request.get_json()
    id = data["id"]

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM routes WHERE route_id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Ruta eliminada exitosamente", "error": False}), 200

"""CRUD"""

# XML Format
@routes.route("/retrieve-xml", methods=["POST"])
def retrieve_xml():
    data = request.get_json()
    id = data["id"]
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT r.route_id, r.name, r.distance, r.active, r.average_speed, r.time, r.truck_id, t.name 
                   FROM routes AS r LEFT JOIN trucks AS t ON r.truck_id = t.truck_id 
                   WHERE r.truck_id = %s""", (id,))
    route = cursor.fetchone()
    cursor.close()

    root = ET.Element("Route")

    route_id_elem = ET.SubElement(root, "ID")
    route_id_elem.text = str(route[0])
    
    route_name_elem = ET.SubElement(root, "Name")
    route_name_elem.text = str(route[1])

    distance_elem = ET.SubElement(root, "Distance")
    distance_elem.text = str(route[2])

    route_name_elem = ET.SubElement(root, "Active")
    route_name_elem.text = str(route[3])

    average_speed_elem = ET.SubElement(root, "AverageSpeed")
    average_speed_elem.text = str(route[4])

    time_elem = ET.SubElement(root, "Time")
    time_elem.text = str(route[5])

    if route[6] is not None:
        truck_elem = ET.SubElement(root, "Truck")
        truck_elem.text = str(route[7])
    
    xml = ET.tostring(root)

    return xml

# JSON Format
@routes.route("/retrieve-json", methods=["POST"])
def retrieve_json():
    data = request.get_json()
    id = data["id"]
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT r.route_id, r.name, r.distance, r.active, r.average_speed, r.time, r.truck_id, t.name 
                   FROM routes AS r LEFT JOIN trucks AS t ON r.truck_id = t.truck_id 
                   WHERE r.truck_id = %s""", (id,))
    route = cursor.fetchone()
    cursor.close()
    j = {}
    j["ID"] = route[0]
    j["Name"] = route[1]
    j["Distance"] = route[2]
    j["Active"] = route[3]
    j["AverageSpeed"] = route[4]
    j["Time"] = route[5]
    if route[6] is not None:
        j["Truck"] = route[7]

    return j

if __name__ == "__main__":
    routes.run(debug=True, host="0.0.0.0", port=5003)
