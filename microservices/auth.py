################### PORT 5001 ###################

# Flask
from flask import Flask, request, url_for, jsonify
from flask_mysqldb import MySQL

# Misc
from dotenv import load_dotenv
import os
load_dotenv()

# Microservice app
auth = Flask(__name__)

auth.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
auth.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
auth.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
auth.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
auth.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(auth)

# Check if the username and password combination is in the database
@auth.route("/check-auth", methods=["POST"])
def check_auth():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    account = cursor.fetchone()
    cursor.close()

    if account:
        return jsonify({"message": "Autenticación exitosa", "id": account[0], "name": account[1], "last": account[2], "error": False}), 200, {"Content-Type": "application/json"}
    else:
        return jsonify({"message": "Fallo de autenticación", "error": False}), 401, {"Content-Type": "application/json"}

# Register a new user into the database
@auth.route("/new-user", methods=["POST"])
def register():
    data = request.get_json()
    name = data["name"]
    lastname = data["lastname"]
    username = data["username"]
    password = data["password"]

    data = [name, lastname, username, password]
    error_message = create_identity(data)

    if error_message:
        return jsonify({"message": error_message, "error": False}), 409, {"Content-Type": "application/json"}

    return jsonify({"message": "Cuenta creada, puede iniciar sesión", "error": False}), 201, {"Content-Type": "application/json"}

# Insert a new identity in the DB
def create_identity(data):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (data[2],))
    existing_user = cursor.fetchone()

    if existing_user:
        return "Nombre de usuario ya existente"

    cursor.execute("""
        INSERT INTO users
        (firstname, lastname, username, password) VALUES
        (%s, %s, %s, %s)
    """, (data[0], data[1], data[2], data[3]))
    mysql.connection.commit()
    cursor.close()

    return None

if __name__ == "__main__":
    auth.run(debug=True, host="0.0.0.0", port=5001)
