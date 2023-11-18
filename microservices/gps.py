################### PORT 5002 ###################

# Flask
from flask import Flask, request, url_for, jsonify
from flask_mysqldb import MySQL
from flask_socketio import SocketIO

# Misc
from dotenv import load_dotenv
import os
load_dotenv()

# Microservice app
gps = Flask(__name__)

gps.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
gps.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
gps.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
gps.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
gps.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(gps)
socketio = SocketIO(gps, cors_allowed_origins="http://localhost:5000")

# WebSocket
@socketio.on("connect")
def handle_connect():
    print("Server is listening...")

@socketio.on("disconnect")
def handle_connect():
    print("Server has disconnected")

@socketio.on("update")
def handle_update():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE trucks
        SET latitude = latitude + (RAND() * 0.01 - 0.005), longitude = longitude + (RAND() * 0.01 - 0.005);
    """)
    mysql.connection.commit()
    cursor.close()

    data = get_truck_locations()
    socketio.emit("updated", list(data))

# Get locations for a map
@gps.route("/get-locations", methods=["GET"])
def get_locations():
    if request.method == "GET":
        locations = get_truck_locations()
        purchases = get_truck_purchases()
        return jsonify({"message": "Ubicaciones recuperadas con éxito", "locations": locations, "purchases": purchases, "error": False}), 200, {"Content-Type": "application/json"}

    return jsonify({"message": "Error de método", "error": True}), 404, {"Content-Type": "application/json"}

# Retrieve all trucks' locations from the database
def get_truck_locations():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT truck_id, name, latitude, longitude
        FROM trucks
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """)
    data = cursor.fetchall()
    cursor.close()

    return data

# Retrieve each truck and purchase association
def get_truck_purchases():
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

if __name__ == "__main__":
    socketio.run(gps, debug=True, host="0.0.0.0", port=5002)
