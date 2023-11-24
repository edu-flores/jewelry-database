################### PORT 5003 ###################

# Flask
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from flask_mysqldb import MySQL
from flask_cors import CORS

# XML generator
import xml.etree.ElementTree as ET

# Misc
from dotenv import load_dotenv
import os
load_dotenv()

# Microservice app
routes = Flask(__name__)
cors = CORS(routes, resources={r"/*": {"origins": "http://localhost:4200"}})

routes.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
routes.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
routes.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
routes.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
routes.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
routes.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(routes)
mysql = MySQL(routes)

"""CRUD"""

# Retrieve routes from the database
@routes.route("/retrieve-routes", methods=["GET"])
@jwt_required()
def retrieve_routes():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT r.route_id, r.name, r.distance, r.active, r.average_speed, r.time, t.name
            FROM routes AS r
            LEFT JOIN trucks AS t
            ON r.truck_id = t.truck_id
        """)
        routes = cursor.fetchall()
        cursor.close()

        response = {
            "routes": [{
                "id": route[0],
                "name": route[1],
                "distance": route[2],
                "active": route[3],
                "averageSpeed": route[4],
                "time": route[5],
                "truckName": route[6]
            } for route in routes],
            "error": False
        }
        return jsonify(response), 200, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Add route to the database
@routes.route("/add-route", methods=["POST"])
@jwt_required()
def add_route():
    try:
        data = request.get_json()
        name = data["name"]
        distance = data["distance"]
        active = data["active"]
        average_speed = data["average_speed"]
        time = data["time"]
        truck_id = data["truck_id"]

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO routes (name, distance, active, average_speed, time, truck_id) VALUES (%s,%s,%s,%s,%s,%s)", (name, distance, active, average_speed, time, truck_id))

        # Get the ID of the inserted route
        cursor.execute("SELECT LAST_INSERT_ID()")
        route_id = cursor.fetchone()[0]

        mysql.connection.commit()
        cursor.close()

        response = {
            "message": "Se agregó correctamente la ruta",
            "route_id": route_id,
            "error": False
        }

        return jsonify(response), 201, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Edit route
@routes.route("/edit-route", methods=["POST"])
@jwt_required()
def edit_route():
    try:
        data = request.get_json()
        id = data["id"]
        name = data["name"]
        distance = data["distance"]
        active = data["active"]
        average_speed = data["average_speed"]
        time = data["time"]
        truck_id = data["truck_id"]

        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE routes SET
            name=%s, distance=%s, active=%s, average_speed=%s, time=%s, truck_id=%s
            WHERE route_id = %s
        """, (name, distance, active, average_speed, time, truck_id, id))
        mysql.connection.commit()
        cursor.close()

        response = {
            "message": "Se actualizó correctamente la ruta",
            "error": False
        }
        return jsonify(response), 200, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Retrieve a single route
@routes.route("/retrieve-route", methods=["GET"])
@jwt_required()
def retrieve_route():
    try:
        id = request.args.get("id")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM routes WHERE route_id = %s", (id,))
        route = cursor.fetchone()
        cursor.close()

        if route:
            response = {
                "route_id": route[0],
                "name": route[1],
                "distance": route[2],
                "active": route[3],
                "average_speed": route[4],
                "time": route[5],
                "truck_id": route[6],
                "error": False
            }
            return jsonify(response), 200, {"Content-Type": "application/json"}

        response = {
            "message": "No se encontró la ruta",
            "error": True
        }
        return jsonify(response), 404, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Delete route from the database
@routes.route("/delete-route", methods=["POST"])
@jwt_required()
def delete_route():
    try:
        data = request.get_json()
        id = data["id"]

        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM routes WHERE route_id = %s", (id,))
        mysql.connection.commit()
        cursor.close()

        response = {
            "message": "Ruta eliminada exitosamente",
            "error": False
        }
        return jsonify(response), 200, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

"""CRUD"""

# XML Format
@routes.route("/retrieve-xml", methods=["GET"])
def retrieve_xml():
    try:
        id = request.args.get("id")
        route = get_route_data(id)

        root = ET.Element("Route")

        route_id_elem = ET.SubElement(root, "ID")
        route_id_elem.text = str(route[0])

        data_elem = ET.SubElement(root, "Data")

        route_name_elem = ET.SubElement(data_elem, "Name")
        route_name_elem.text = str(route[1])

        distance_elem = ET.SubElement(data_elem, "Distance")
        distance_elem.text = str(route[2])

        route_name_elem = ET.SubElement(data_elem, "Active")
        route_name_elem.text = str(route[3])

        average_speed_elem = ET.SubElement(data_elem, "AverageSpeed")
        average_speed_elem.text = str(route[4])

        time_elem = ET.SubElement(data_elem, "Time")
        time_elem.text = str(route[5])

        truck_elem = ET.SubElement(root, "Truck")

        truck_id_elem = ET.SubElement(truck_elem, "TruckID")
        truck_id_elem.text = str(route[7])

        truck_name_elem = ET.SubElement(truck_elem, "TruckName")
        truck_name_elem.text = str(route[8])

        xml = ET.tostring(root)

        return xml
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# JSON Format
@routes.route("/retrieve-json", methods=["GET"])
def retrieve_json():
    try:
        id = request.args.get("id")
        route = get_route_data(id)

        j = {
            "id": route[0],
            "data": {
                "name": route[1],
                "distance": route[2],
                "active": route[3] == "1",
                "averageSpeed": route[4],
                "time": route[5]
            },
            "truck": {
                "id": route[7],
                "name": route[8]
            }
        }

        return jsonify(j)
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Route data query
def get_route_data(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT routes.*, trucks.truck_id, trucks.name
            FROM routes JOIN trucks ON routes.truck_id = trucks.truck_id
            WHERE route_id = %s
        """, (id,))
        route = cursor.fetchone()
        cursor.close()

        return route
    except Exception as e:
        print(f"Error in get_route_data: {str(e)}")
        return None

if __name__ == "__main__":
    routes.run(debug=True, host="0.0.0.0", port=5003)
