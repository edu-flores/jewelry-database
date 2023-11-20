# Flask
from flask import request, render_template, redirect, url_for, session, Response
from interface import app, mysql

# Misc
import requests

# Manage routes
@app.route("/admin/routes")
def routes():
    if "id" not in session:
        return redirect(url_for("sign_in", msg="Inicio de sesión requerido"))

    routes = requests.get("http://localhost:5003/retrieve-routes", headers={"Authorization": f"Bearer {session['token']}"})
    routes_data = routes.json()

    if routes.status_code == 200:
        return render_template("routes.html", data=1, message=request.args.get("msg", ""), routes=routes_data["routes"])
    else:
        return render_template("routes.html", data=0, message=request.args.get("msg", ""))

"""CRUD"""

# Add route template
@app.route("/admin/route-add-form")
def route_add_form():
    trucks = requests.get("http://localhost:5004/retrieve-trucks", headers={"Authorization": f"Bearer {session['token']}"});
    trucks_data = trucks.json()

    # Get only the id and name of the trucks
    filtered_trucks = [{"id": truck["id"], "name": truck["name"]} for truck in trucks_data["trucks"]]
    return render_template("route-form.html", data=0, trucks=filtered_trucks)

# Add route into the DB
@app.route("/route-add", methods=["POST"])
def route_add():
    name = request.form.get("name")
    distance = int(request.form.get("distance"))
    time = int(request.form.get("time"))
    average_speed = int(request.form.get("average_speed"))
    active = int(request.form.get("active"))
    truck_id = request.form.get("truck")

    route_response = requests.post("http://localhost:5003/add-route", json={"name": name, "distance": distance, "time": time, "average_speed": average_speed, "active": active, "truck_id": truck_id}, headers={"Authorization": f"Bearer {session['token']}"})
    response_data = route_response.json()

    return redirect(url_for("routes", msg=response_data["message"]))

# Update route in the DB
@app.route("/route-udpate/<int:id>", methods=["POST"])
def route_update(id):
    name = request.form.get("name")
    distance = int(request.form.get("distance"))
    time = int(request.form.get("time"))
    average_speed = int(request.form.get("average_speed"))
    active = int(request.form.get("active"))
    truck_id = request.form.get("truck")

    route_response = requests.post("http://localhost:5003/edit-route", json={"id": id, "name": name, "distance": distance, "time": time, "average_speed": average_speed, "active": active, "truck_id": truck_id}, headers={"Authorization": f"Bearer {session['token']}"})
    response_data = route_response.json()

    return redirect(url_for("routes", msg=response_data["message"]))

# Update route template
@app.route("/admin/route-edit/<int:id>")
def route_edit(id):
    route = requests.get("http://localhost:5003/retrieve-route", params={"id": id}, headers={"Authorization": f"Bearer {session['token']}"})
    route_data = route.json()

    trucks = requests.get("http://localhost:5004/retrieve-trucks", headers={"Authorization": f"Bearer {session['token']}"})
    trucks_data = trucks.json()

    # Get only the id and name of the trucks
    filtered_trucks = [{"id": truck["id"], "name": truck["name"]} for truck in trucks_data["trucks"]]

    if route.status_code == 200 and trucks.status_code == 200:
        return render_template("route-form.html", data=1, route=route_data, trucks=filtered_trucks)
    else:
        return render_template("route-form.html", error=1)

# Remove route from the DB
@app.route("/admin/route-delete/<int:id>")
def route_delete(id):
    route = requests.post("http://localhost:5003/delete-route", json={"id": id}, headers={"Authorization": f"Bearer {session['token']}"})

    routes = requests.get("http://localhost:5003/retrieve-routes", headers={"Authorization": f"Bearer {session['token']}"})
    routes_data = routes.json()

    if route.status_code == 200 and routes.status_code == 200:
        return redirect(url_for("routes", msg="Ruta eliminada exitosamente"))
    else:
        return redirect(url_for("routes", msg="Ocurrió un error y la ruta no pudo ser eliminada"))

"""CRUD"""

"""XML & JSON"""

# XML
@app.route("/admin/routes/xml/<int:id>")
def xml_route(id):
    xml = requests.get("http://localhost:5003/retrieve-xml", params={"id": id})

    return Response(xml, content_type="application/xml")

# JSON
@app.route("/admin/routes/json/<int:id>")
def json_route(id):
    json = requests.get("http://localhost:5003/retrieve-json", params={"id": id})
    return Response(json, content_type="application/json")

"""XML & JSON"""
