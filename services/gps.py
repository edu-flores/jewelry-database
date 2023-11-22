################### PORT 5002 ###################

# Flask
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
from flask_cors import CORS

# Misc
from dotenv import load_dotenv
import os
load_dotenv()

# Microservice app
gps = Flask(__name__)
cors = CORS(gps, resources={r"/*": {"origins": "http://localhost:4200"}})

gps.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
gps.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
gps.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
gps.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
gps.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
gps.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(gps)
mysql = MySQL(gps)
socketio = SocketIO(gps, cors_allowed_origins="http://localhost:5000")

# WebSocket
@socketio.on("connect")
def handle_connect():
    print("Server is listening...")

@socketio.on("disconnect")
def handle_disconnect():
    print("Server has disconnected")

@socketio.on("update")
def handle_update():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("CALL UpdateMap()")
        mysql.connection.commit()
        cursor.close()

        data = get_truck_locations()
        trucks = [{
            "id": truck[0],
            "name": truck[1],
            "latitude": truck[2],
            "longitude": truck[3]
        } for truck in data]

        data = get_gps_data()
        air = [{
            "quality": record[0],
            "contaminants": record[1] == 1,
            "latitude": record[2],
            "longitude": record[3]
        } for record in data]

        socketio.emit("updated", {"trucks": trucks, "air": air})
    except Exception as e:
        print(f"Error in handle_update: {str(e)}")

# Get locations for a map
@gps.route("/get-locations", methods=["GET"])
@jwt_required()
def get_locations():
    try:
        trucks = get_truck_locations()
        air_data = get_gps_data()

        response = {
            "message": "Ubicaciones recuperadas con éxito",
            "trucks": [{
                "id": truck[0],
                "name": truck[1],
                "latitude": truck[2],
                "longitude": truck[3]
            } for truck in trucks],
            "air": [{
                "quality": record[0],
                "contaminants": record[1] == 1,
                "latitude": record[2],
                "longitude": record[3]
            } for record in air_data],
            "error": False
        }
        return jsonify(response), 200, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Get purchases and their statuses
@gps.route("/get-purchases", methods=["GET"])
@jwt_required()
def get_purchases():
    try:
        purchases = get_truck_purchases()

        if purchases:
            response = {
                "message": "Compras recuperadas con éxito",
                "purchases": [{
                    "truck": purchase[0],
                    "id": purchase[1],
                    "status": purchase[2]
                } for purchase in purchases],
                "error": False
            }
            return jsonify(response), 200, {"Content-Type": "application/json"}

        response = {
            "message": "No se encontraron compras",
            "error": True
        }
        return jsonify(response), 404, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Retrieve all trucks' locations from the database
def get_truck_locations():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT truck_id, name, latitude, longitude
            FROM trucks
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        """)
        data = cursor.fetchall()
        cursor.close()

        return data
    except Exception as e:
        print(f"Error in get_truck_locations: {str(e)}")
        return []

# Retrieve all trucks' locations from the database
def get_gps_data():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT air_quality, contaminants, latitude, longitude
            FROM gps_data
            WHERE date > NOW() - INTERVAL 20 SECOND
        """)
        data = cursor.fetchall()
        cursor.close()

        return data
    except Exception as e:
        print(f"Error in get_truck_locations: {str(e)}")
        return []

# Retrieve each truck and purchase association
def get_truck_purchases():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT t.name, p.purchase_id, p.status
            FROM trucks t
            JOIN purchase p
            ON t.truck_id = p.truck_id;
        """)
        data = cursor.fetchall()
        cursor.close()

        return data
    except Exception as e:
        print(f"Error in get_truck_purchases: {str(e)}")
        return []

if __name__ == "__main__":
    socketio.run(gps, debug=True, host="0.0.0.0", port=5002)
