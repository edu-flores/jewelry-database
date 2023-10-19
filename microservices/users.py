# Flask
from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL

# Misc
from dotenv import load_dotenv
import os
load_dotenv()

# Microservice app
users_app = Flask(__name__)

users_app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
users_app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
users_app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
users_app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
users_app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

# Login user
@users_app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
    account = cursor.fetchone()
    cursor.close()

    if account:
        session["id"] = account[0]
        session["name"] = account[1] + " " + account[2]
        return redirect("/vehicles")
    else:
        return redirect(url_for("sign_in", msg="Credenciales incorrectas"))

# Logout user
@users_app.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("name", None)
    return redirect(url_for("sign_in", msg="Sesión cerrada"))

# Sign in web page
@users_app.route("/sign-in")
def sign_in():
    return render_template("sign_in.html", message=request.args.get("msg", ""))

# Sign up web page
@users_app.route("/sign-up")
def sign_up():
    return render_template("sign_up.html", message=request.args.get("msg", ""))

# Register a new identity
@users_app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]

    data = [name, lastname, username, password]
    error_message = create_identity(data)

    if error_message:
        return redirect(url_for("sign_up", msg=error_message))

    return redirect(url_for("sign_in", msg="Cuenta creada, puede iniciar sesión"))

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
    users_app.run(debug=True, port=5001)