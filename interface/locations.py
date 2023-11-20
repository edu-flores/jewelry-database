# Flask
from flask import render_template, redirect, url_for, session
from interface import app

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
    locations_response = requests.get("http://localhost:5002/get-locations", headers={"Authorization": f"Bearer {session['token']}"})
    purchases_response = requests.get("http://localhost:5002/get-purchases", headers={"Authorization": f"Bearer {session['token']}"})

    locations_data = locations_response.json()
    purchases_data = purchases_response.json()

    return render_template("map.html", maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"), locations=locations_data["locations"], purchases=purchases_data["purchases"])
