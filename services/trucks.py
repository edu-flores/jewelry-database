################### PORT 5004 ###################

# Flask
from flask import Flask, Response, request, jsonify
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
trucks = Flask(__name__)
cors = CORS(trucks, resources={r"/*": {"origins": "http://127.0.0.1:4200"}})

trucks.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
trucks.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
trucks.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
trucks.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
trucks.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
trucks.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(trucks)
mysql = MySQL(trucks)

"""CRUD"""

# Get all trucks from the database
@trucks.route("/retrieve-trucks", methods=["GET"])
@jwt_required()
def retrieve_trucks():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT t.truck_id, t.name, t.total_distance, ((t.total_distance / 25) * 2.68) AS total_CO2, t.average_trip_distance, ((t.average_trip_distance / 25) * 2.68) AS average_CO2, t.latitude, t.longitude
            FROM trucks AS t
        """)
        trucks = cursor.fetchall()
        cursor.close()

        response = {
            "trucks": [{
                "id": truck[0],
                "name": truck[1],
                "totalDistance": truck[2],
                "totalCO2": float(truck[3]),
                "averageTripDistance": truck[4],
                "averageCO2": float(truck[5]),
                "latitude": truck[6],
                "longitude": truck[7]
            } for truck in trucks],
            "message": "Camiones recuperados con éxito",
            "error": False
        }
        return jsonify(response), 200, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Add a new truck to the database
@trucks.route("/add-truck", methods=["POST"])
@jwt_required()
def add_truck():
    try:
        data = request.get_json()
        name = data["name"]
        total_distance = data["totalDistance"]
        average_trip_distance = data["averageTripDistance"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO trucks (name, total_distance, average_trip_distance, latitude, longitude) VALUES (%s,%s,%s,%s,%s)", (name, total_distance, average_trip_distance, latitude, longitude))

        # Get the ID of the inserted truck
        cursor.execute("SELECT LAST_INSERT_ID()")
        truck_id = cursor.fetchone()[0]

        mysql.connection.commit()
        cursor.close()

        response = {
            "message": "Se agregó correctamente el camión",
            "truckId": truck_id,
            "error": False
        }
        return jsonify(response), 201, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Edit an existing truck
@trucks.route("/edit-truck", methods=["POST"])
@jwt_required()
def edit_truck():
    try:
        data = request.get_json()
        id = data["id"]
        name = data["name"]
        total_distance = data["totalDistance"]
        average_trip_distance = data["averageTripDistance"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE trucks SET
            name=%s, total_distance=%s, average_trip_distance=%s, latitude=%s, longitude=%s
            WHERE truck_id = %s """, (name, total_distance, average_trip_distance, latitude, longitude, id))
        mysql.connection.commit()
        cursor.close()

        response = {
            "message": "Se actualizó correctamente el camión",
            "error": False
        }
        return jsonify(response), 200, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Retrieve a single truck
@trucks.route("/retrieve-truck", methods=["GET"])
@jwt_required()
def retrieve_truck():
    try:
        id = request.args.get("id")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM trucks WHERE truck_id = %s", (id,))
        truck = cursor.fetchone()
        cursor.close()

        if truck:
            response = {
                "truck_id": truck[0],
                "name": truck[1],
                "totalDistance": truck[2],
                "averageTripDistance": truck[3],
                "latitude": truck[4],
                "longitude": truck[5],
                "error": False
            }
            return jsonify(response), 200, {"Content-Type": "application/json"}

        response = {
            "message": "No se encontró el camión",
            "error": True
        }
        return jsonify(response), 404, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Delete a truck from the database
@trucks.route("/delete-truck", methods=["POST"])
@jwt_required()
def delete_truck():
    try:
        data = request.get_json()
        id = data["id"]

        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM trucks WHERE truck_id = %s", (id,))
        mysql.connection.commit()
        cursor.close()

        response = {
            "message": "Camión eliminado exitosamente",
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

# Get ambient conditions
@trucks.route("/get-conditions")
@jwt_required()
def get_conditions():
    try:
        trucks_co2 = get_trucks_co2()
        short_long_stops = get_short_long_stops()
        samples_data = get_samples_data()
        environmental_data = get_environmental_data()

        if trucks_co2 and short_long_stops and samples_data and environmental_data:
            response = {
                "ambient": {
                    "trucksCO2": [{
                        "name": truck[0],
                        "totalCO2": float(truck[1])
                    } for truck in trucks_co2],
                    "shortLongStops": {
                        "short": [{
                            "time": short[0],
                            "count": short[1]
                        } for short in short_long_stops[0]],
                        "long": [{
                            "time": long[0],
                            "count": long[1]
                        } for long in short_long_stops[1]],
                    },
                    "samplesData": [{
                        "time": sample[0],
                        "distance": int(sample[1]),
                        "speed": sample[2]
                    } for sample in samples_data],
                    "environmentalData": [{
                        "time": record[0],
                        "temperature": record[1],
                        "humidity": record[2],
                        "precipitation": record[3],
                        "windSpeed": record[4],
                        "pressure": record[5]
                    } for record in environmental_data]
                },
                "warning": sum(float(truck[1]) for truck in trucks_co2) >= 30000,
                "message": "Datos recuperados con éxito",
                "error": False
            }
            return jsonify(response), 200, {"Content-Type": "application/json"}

        response = {
            "message": "No se encontraron datos",
            "error": True
        }
        return jsonify(response), 404, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Get CO2 per truck
def get_trucks_co2():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name, ((total_distance / 25) * 2.68) AS total_CO2 FROM trucks")
        trucks_co2 = cursor.fetchall()
        cursor.close()

        return trucks_co2
    except Exception as e:
        return None

# Get short and long stops
def get_short_long_stops():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT DATE_FORMAT(start_time, '%Y-%m') AS month, COUNT(*) AS number_of_short_stops
            FROM short_stops
            WHERE YEAR(start_time) = YEAR(CURDATE())
            GROUP BY month;
        """)
        short = cursor.fetchall()
        cursor.execute("""
            SELECT DATE_FORMAT(start_time, '%Y-%m') AS month, COUNT(*) AS number_of_long_stops
            FROM long_stops
            WHERE YEAR(start_time) = YEAR(CURDATE())
            GROUP BY month
        """)
        long = cursor.fetchall()
        cursor.close()

        return short, long
    except Exception as e:
        return None

# Get samples data
def get_samples_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT DATE_FORMAT(datetime, '%Y-%m') AS month, SUM(distance) AS total_distance, AVG(speed) AS average_speed
            FROM samples
            WHERE YEAR(datetime) = YEAR(CURDATE())
            GROUP BY month
        """)
        samples_data = cursor.fetchall()
        cursor.close()

        return samples_data
    except Exception as e:
        return None

# Get environmental data
def get_environmental_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT
                DATE_FORMAT(date, '%Y-%m') AS month,
                AVG(temperature) AS avg_temperature,
                AVG(humidity) AS avg_humidity,
                AVG(precipitation) AS avg_precipitation,
                AVG(wind_speed) AS avg_wind_speed,
                AVG(pressure) AS avg_pressure
            FROM
                environmental_data
            WHERE
                YEAR(date) = YEAR(CURDATE())
            GROUP BY
                month
        """)
        environmental_data = cursor.fetchall()
        cursor.close()

        return environmental_data
    except Exception as e:
        return None

# XML Format
@trucks.route("/retrieve-xml", methods=["GET"])
def retrieve_xml():
    try:
        id = request.args.get("id")
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

        return Response(xml, content_type="application/xml")
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# JSON Format
@trucks.route("/retrieve-json", methods=["GET"])
def retrieve_json():
    try:
        id = request.args.get("id")
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

        return jsonify(j)
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Truck data query
def get_truck_data(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT t.truck_id, t.name, t.total_distance, ((t.total_distance / 25) * 2.68) AS total_CO2, t.average_trip_distance, ((t.average_trip_distance / 25) * 2.68) AS average_CO2, t.latitude, t.longitude
            FROM trucks AS t
            WHERE t.truck_id = %s
        """, (id,))
        truck = cursor.fetchone()
        cursor.close()

        return truck
    except Exception as e:
        print(f"Error in get_truck_data: {str(e)}")
        return None

if __name__ == "__main__":
    trucks.run(debug=True, host="0.0.0.0", port=5004)
