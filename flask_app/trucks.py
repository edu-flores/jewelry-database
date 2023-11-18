# Flask
from flask import request, render_template, redirect, url_for, session, Response
from flask_app import app, mysql

# Misc
import requests

# Manage trucks
@app.route("/admin/trucks")
def trucks():
    if "id" not in session:
        return redirect(url_for("sign_in", msg="Inicio de sesión requerido"))

    trucks = requests.get("http://localhost:5004/retrieve-trucks")
    trucks_data = trucks.json()

    if trucks.status_code == 200:
        return render_template("trucks.html", data=1, message=request.args.get("msg", ""), trucks=trucks_data["trucks"], environment=trucks_data["environment"])
    else:
        return render_template("trucks.html", data=0, message=request.args.get("msg", ""))

"""CRUD"""

# Add truck template
@app.route("/admin/truck-add-form")
def truck_add_form():
    return render_template("truck-form.html", data=0)

# Add truck into the DB
@app.route("/truck-add", methods=["POST"])
def truck_add():
    name = request.form.get("name")
    total_distance = int(request.form.get("total_distance"))
    average_trip_distance = int(request.form.get("average_trip_distance"))
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    truck_response = requests.post("http://localhost:5004/add-truck", json={"name": name, "total_distance": total_distance, "average_trip_distance": average_trip_distance, "latitude": latitude, "longitude": longitude})
    response_data = truck_response.json()

    return redirect(url_for("trucks", msg=response_data["message"]))

# Update truck in the DB
@app.route("/truck-update/<int:id>", methods=["POST"])
def truck_update(id):
    name = request.form.get("name")
    total_distance = int(request.form.get("total_distance"))
    average_trip_distance = int(request.form.get("average_trip_distance"))
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    truck_response = requests.post("http://localhost:5004/edit-truck", json={"id": id,"name": name, "total_distance": total_distance, "average_trip_distance": average_trip_distance, "latitude": latitude, "longitude": longitude})
    response_data = truck_response.json()

    return redirect(url_for("trucks", msg=response_data["message"]))

# Update truck template
@app.route("/admin/truck-edit/<int:id>")
def truck_edit(id):
    truck = requests.get("http://localhost:5004/retrieve-truck", params={"id":id})
    truck_data = truck.json()

    trucks = requests.get("http://localhost:5004/retrieve-trucks")
    trucks_data = trucks.json()

    if truck.status_code == 200 and trucks.status_code == 200:
        return render_template("truck-form.html", data=1, truck=truck_data, trucks=trucks_data)
    else:
        return render_template("truck-form.html", error=1)

# Remove truck from the DB
@app.route("/admin/truck-delete/<int:id>")
def truck_delete(id):
    truck = requests.post("http://localhost:5004/delete-truck", json={"id": id})

    trucks = requests.get("http://localhost:5004/retrieve-trucks")
    trucks_data = trucks.json()

    if truck.status_code == 200 and trucks.status_code == 200:
        return redirect(url_for("trucks", msg="Camión eliminado exitosamente"))
    else:
        return redirect(url_for("trucks", msg="Este camión está siendo utilizado por una ruta, verifique la ruta para eliminarlo"))

"""CRUD"""

"""XML & JSON"""

# XML
@app.route("/admin/trucks/xml/<int:id>")
def xml_truck(id):
    xml = requests.get("http://localhost:5004/retrieve-xml", params={"id": id})

    return Response(xml, content_type="application/xml")

# JSON
@app.route("/admin/trucks/json/<int:id>")
def json_truck(id):
    json = requests.get("http://localhost:5004/retrieve-json", params={"id": id})

    return Response(json, content_type="application/json")

"""XML & JSON"""
