################### PORT 5002 ###################

# Flask
from flask import Flask, request, url_for, jsonify
from flask_mysqldb import MySQL

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

# Get locations for a map
@gps.route("/get-locations", methods=["GET"])
def get_locations():
    if request.method == "GET":
        data = get_truck_locations()
        return jsonify({"message": "Ubicaciones recuperadas con éxito", "data": data, "error": False}), 200

    return jsonify({"message": "Error de método", "error": True}), 404

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

if __name__ == "__main__":
    gps.run(debug=True, host="0.0.0.0", port=5002)
