################### Correr microservicio en puerto 5001
# Flask
from flask import Flask, redirect, request, url_for, session, jsonify
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
    username = request.form["username"]
    password = request.form["password"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
    account = cursor.fetchone()
    cursor.close()

    if account:
        session["id"] = account[0]
        session["name"] = account[1] + " " + account[2]
        return jsonify({"message": "Autenticación exitosa", "error": False}), 200
    else:
        return jsonify({"message": "Fallo de autenticación", "error": False}), 401

# Register a new user into the database
@auth.route("/new-user", methods=["POST"])
def register():
    name = request.form["name"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]

    data = [name, lastname, username, password]
    error_message = create_identity(data)

    if error_message:
        return jsonify({"message": error_message, "error": False}), 409

    return jsonify({"message": "Cuenta creada, puede iniciar sesión", "error": False}), 200

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
        (%s, %s, %s, %s, 0, current_timestamp(), current_timestamp())
    """, (data[0], data[1], data[2], data[3]))
    mysql.connection.commit()
    cursor.close()

    return None

if __name__ == "__main__":
    auth.run(debug=True, host="0.0.0.0", port=5001)