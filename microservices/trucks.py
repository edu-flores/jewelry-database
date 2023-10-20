################### PORT 5004 ###################

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
truck = Flask(__name__)

truck.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
truck.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
truck.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
truck.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
truck.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(truck)

"""CRUD"""

@truck.route("/retrieve-trucks", methods=["POST"])
def retrieve_trucks():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT t.truck_id, t.name, t.total_distance, ((t.total_distance / 25) * 2.68) AS total_CO2, t.average_trip_distance, ((t.average_trip_distance / 25) * 2.68) AS average_CO2, t.latitude, t.longitude FROM trucks AS t")
    trucks = cursor.fetchall()
    cursor.close()
    if truck:
        trucksJSON = [{"id": truck[0], "name": truck[1], "total_distance": truck[2], "total_CO2": truck[3], "average_trip_distance": truck[4], "average_CO2": truck[5], "latitude": truck[6], "longitude": truck[7], "error": False} for truck in trucks]
        return jsonify(trucksJSON), 200
    else:
        return jsonify({"error": False}), 401

@truck.route("/add-truck", methods=["POST"])
def add_truck():
    data = request.get_json()
    name = data["name"]
    total_distance = data["total_distance"]
    average_trip_distance = data["average_trip_distance"]
    latitude = data["latitude"]
    longitude = data["longitude"]

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO trucks (name, total_distance, average_trip_distance, latitude, longitude) VALUES (%s,%s,%s,%s,%s)", (name, total_distance, average_trip_distance, latitude, longitude))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Se agregó correctamente el camión", "error": False}), 200

@truck.route("/edit-truck", methods=["POST"])
def edit_truck():
    data = request.get_json()
    id = data["id"]
    name = data["name"]
    total_distance = data["total_distance"]
    average_trip_distance = data["average_trip_distance"]
    latitude = data["latitude"]
    longitude = data["longitude"]

    cursor = mysql.connection.cursor()
    cursor.execute("""UPDATE trucks SET 
        name=%s, total_distance=%s, average_trip_distance=%s, latitude=%s, longitude=%s
        WHERE truck_id = %s """, (name, total_distance, average_trip_distance, latitude, longitude, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Se actualizó correctamente el camión", "error": False}), 200

@truck.route("/retrieve-truck", methods=["POST"])
def retrieve_truck():
    data = request.get_json()
    id = data["id"]
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM trucks WHERE truck_id = %s", (id,))
    truck = cursor.fetchone()
    cursor.close()

    if truck:
        return jsonify({"truck_id": truck[0], "name": truck[1], "total_distance": truck[2], "average_trip_distance": truck[3], "latitude": truck[4], "longitude": truck[5]}), 200
    else:
        return jsonify({"error", False}), 401

@truck.route("/delete-truck", methods=["POST"])
def delete_truck():
    data = request.get_json()
    id = data["id"]

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM trucks WHERE truck_id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Camión eliminada exitosamente", "error": False}), 200

"""CRUD"""

# XML Format
@truck.route("/retrieve-xml", methods=["POST"])
def retrieve_xml():
    data = request.get_json()
    id = data["id"]
    truck = get_truck_data(id)

    root = ET.Element("Truck")

    truck_id_elem = ET.SubElement(root, "ID")
    truck_id_elem.text = str(truck[0])

    data_elem = ET.SubElement(root, "Data")

    truck_name_elem = ET.SubElement(data_elem, "Name")
    truck_name_elem.text = str(truck[1])

    total_distance_elem = ET.SubElement(data_elem, "TotalDistance")
    total_distance_elem.text = str(truck[2])

    total_co2_elem = ET.SubElement(data_elem, "TotalCO2Emitted")
    total_co2_elem.text = str(truck[3])

    average_distance_elem = ET.SubElement(data_elem, "AverageDistance")
    average_distance_elem.text = str(truck[4])

    average_co2_elem = ET.SubElement(data_elem, "AverageCO2Emitted")
    average_co2_elem.text = str(truck[5])
    
    location_elem = ET.SubElement(root, "Location")

    latitude_elem = ET.SubElement(location_elem, "Latitude")
    latitude_elem.text = str(truck[6])

    longitude_elem = ET.SubElement(location_elem, "Longitude")
    longitude_elem.text = str(truck[7])

    xml = ET.tostring(root)

    return xml

# JSON Format
@truck.route("/retrieve-json", methods=["POST"])
def retrieve_json():
    data = request.get_json()
    id = data["id"]
    truck = get_truck_data(id)

    j = {
        "id": truck[0],
        "data": {
            "name": truck[1],
            "totalDistance": truck[2],
            "totalCO2": truck[3],
            "averageDistance": truck[4],
            "averageCO2": truck[5],
        },
        "location": {
            "latitude": truck[6],
            "longitude": truck[7],
        }
    }

    return j

# Truck data query
def get_truck_data(id):
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT t.truck_id, t.name, t.total_distance, ((t.total_distance / 25) * 2.68) AS total_CO2, t.average_trip_distance, ((t.average_trip_distance / 25) * 2.68) AS average_CO2, t.latitude, t.longitude 
                   FROM trucks AS t
                   WHERE t.truck_id = %s""",(id,))
    truck = cursor.fetchone()
    cursor.close()

    return truck

if __name__ == "__main__":
    truck.run(debug=True, host="0.0.0.0", port=5004)
