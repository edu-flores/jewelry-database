# Flask
from flask import request, render_template, redirect, url_for, session
from flask_app import app

# Misc
import requests

# Sign in template
@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html", message=request.args.get("msg", ""))

# Sign up template
@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html", message=request.args.get("msg", ""))

# Log in user to the admin app
@app.route("/login", methods=["POST"])
def login():
    # Get credentials
    username = request.form["username"]
    password = request.form["password"]

    # Attempt auth with microservice
    auth_response = requests.post("http://localhost:5001/check-auth", json={"username": username, "password": password})
    response_data = auth_response.json()

    # Response
    if auth_response.status_code == 200:
        session["id"] = response_data["id"]
        session["name"] = response_data["name"] + " " + response_data["last"]
        return redirect("/admin/vehicles")
    else:
        return redirect(url_for("sign_in", msg="Credenciales incorrectas"))

# Logout user
@app.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("name", None)
    return redirect(url_for("sign_in", msg="Sesión cerrada"))

# Register a new account
@app.route("/register", methods=["POST"])
def register():
    # Get credentials
    name = request.form["name"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]

    # Attempt auth with microservice
    auth_response = requests.post("http://localhost:5001/new-user", json={"name": name, "lastname": lastname, "username": username, "password": password})
    response_data = auth_response.json()
    print(response_data)

    # Response
    if auth_response.status_code == 200:
        return redirect(url_for("sign_in", msg=response_data["message"]))
    else:
        return redirect(url_for("sign_up", msg=response_data["message"]))

