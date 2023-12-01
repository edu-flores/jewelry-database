################### PORT 5001 ###################

# Flask
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_mysqldb import MySQL
from flask_cors import CORS

# Misc
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import os
load_dotenv()

# Microservice app
auth = Flask(__name__)
cors = CORS(auth, resources={r"/*": {"origins": "http://127.0.0.1:4200"}})

auth.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
auth.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
auth.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
auth.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
auth.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
auth.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
auth.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

jwt = JWTManager(auth)
mysql = MySQL(auth)

# Check if the username and password combination is in the database
@auth.route("/check-auth", methods=["POST"])
def check_auth():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()
        cursor.close()

        if account and bcrypt.checkpw(password.encode("utf-8"), account[4].encode("utf-8")):
            # JWT
            access_token = create_access_token(identity=username)
            expires = auth.config["JWT_ACCESS_TOKEN_EXPIRES"]
            expiration_time = (auth.config["JWT_ACCESS_TOKEN_EXPIRES"] + datetime.utcnow()).isoformat()

            response = {
                "message": "Autenticación exitosa",
                "token": access_token,
                "expires": expiration_time,
                "id": account[0],
                "name": account[1],
                "last": account[2],
                "admin": account[5],
                "error": False
            }
            return jsonify(response), 200, {"Content-Type": "application/json"}

        response = {
            "message": "Fallo de autenticación",
            "error": False
        }
        return jsonify(response), 401, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Register a new user into the database
@auth.route("/new-user", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data["name"]
        lastname = data["lastname"]
        username = data["username"]
        password = data["password"]

        error_message = create_identity(name, lastname, username, password)
        if error_message:
            response = {
                "message": error_message,
                "error": False
            }
            return jsonify(response), 409, {"Content-Type": "application/json"}

        response = {
            "message": "Cuenta creada, puede iniciar sesión",
            "error": False
        }
        return jsonify(response), 201, {"Content-Type": "application/json"}
    except Exception as e:
        response = {
            "message": f"Internal Server Error: {str(e)}",
            "error": True
        }
        return jsonify(response), 500, {"Content-Type": "application/json"}

# Insert a new identity in the DB
def create_identity(name, lastname, username, password):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Nombre de usuario ya existente"

        # Hash and salt the password before storing it
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        cursor.execute("""
            INSERT INTO users
            (firstname, lastname, username, password, admin) VALUES
            (%s, %s, %s, %s, 1)
        """, (name, lastname, username, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return None
    except Exception as e:
        return f"Internal Server Error: {str(e)}"

if __name__ == "__main__":
    auth.run(debug=True, host="0.0.0.0", port=5001)
