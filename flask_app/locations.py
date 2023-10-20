# Flask
from flask import render_template, redirect, url_for, session
from flask_app import app

# Misc
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Map showing different trucks' location
@app.route("/admin/map")
def truck_map():
    if "id" not in session:
        return redirect(url_for("sign_in", msg="Inicio de sesión requerido"))

    # Access GPS microservice
    auth_response = requests.get("http://localhost:5002/get-locations")
    response_data = auth_response.json()

    return render_template("map.html", maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"), locations=response_data["data"])
