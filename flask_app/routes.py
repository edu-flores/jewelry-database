# Flask
from flask import request, render_template, redirect, url_for, Response
from flask_app import app, mysql

# Misc
import requests

# Manage routes
@app.route("/routes")
def routes():
    routes = requests.post("http://localhost:5003/retrieve_routes")
    routes_data = routes.json()

    if routes.status_code == 200:
        return render_template("routes.html", data=1, routes=routes_data)
    else:
        return render_template("routes.html", data=0, message=request.args.get("msg", ""))

"""CRUD"""
# Add route template
@app.route("/route_add_form")
def route_add_form():
    trucks = requests.post("http://localhost:5003/retrieve_trucks")
    trucks_data = trucks.json()
    return render_template("route-form.html",data=0,trucks=trucks_data)

# Add route into the DB
@app.route("/route_add", methods=["POST"])
def route_add():
    name = request.form.get("name")
    distance = int(request.form.get("distance"))
    time = int(request.form.get("time"))
    average_speed = int(request.form.get("average_speed"))
    activo = int(request.form.get("activo"))
    truck_id = -1
    if activo:
        truck_id = request.form.get("truck")

    msg = requests.post("http://localhost:5003/add_route", json={"name": name, "distance": distance, "time": time, "average_speed": average_speed, "activo":activo, "truck_id":truck_id})

    return redirect(url_for("routes"))

# Update route in the DB
@app.route("/route_udpate/<int:id>", methods=["POST"])
def route_update(id):
    name = request.form.get("name")
    distance = int(request.form.get("distance"))
    time = int(request.form.get("time"))
    average_speed = int(request.form.get("average_speed"))
    activo = int(request.form.get("activo"))
    truck_id = -1
    if activo:
        truck_id = request.form.get("truck")

    msg = requests.post("http://localhost:5003/edit_route", json={"id":id, "name": name, "distance": distance, "time": time, "average_speed": average_speed, "activo":activo, "truck_id":truck_id})
    
    return redirect(url_for("routes"))

# Update route template
@app.route("/route_edit/<int:id>")
def route_edit(id):
    route = requests.post("http://localhost:5003/retrieve_route", json={"id":id})
    route_data = route.json()
    trucks = requests.post("http://localhost:5003/retrieve_trucks")
    trucks_data = trucks.json()

    if route.status_code == 200 and trucks.status_code == 200:
        return render_template("route-form.html",data=1,route=route_data,trucks=trucks_data)
    else:
        return render_template("route-form.html",error=1)

# Remove route from the DB
@app.route("/route_delete/<int:id>")
def route_delete(id):
    route = requests.post("http://localhost:5003/delete_route", json={"id":id})

    routes = requests.post("http://localhost:5003/retrieve_routes")
    routes_data = routes.json()

    if route.status_code == 200:
        if routes.status_code == 200:
            return render_template("routes.html",msg="Ruta eliminada exitosamente",data=1,routes=routes_data)
        else:
            return render_template("routes.html",msg="Ruta eliminada exitosamente",data=0)
    else:
        if routes.status_code == 200:
            return render_template("routes.html",msg="Ocurrio un error y la ruta no pudo ser eliminada")
        else:
            return render_template("routes.html",msg="Ocurrio un error y la ruta no pudo ser eliminada",data=0)
"""CRUD"""

"""XML & JSON"""

# XML
@app.route("/routes/xml/<int:id>")
def xml_route(id):
    xml = requests.post("http://localhost:5003/retrieve_xml", json={"id":id})

    return Response(xml, content_type="text/xml")

# JSON
@app.route("/routes/json/<int:id>")
def json_route(id):
    json = requests.post("http://localhost:5003/retrieve_json", json={"id":id})
    return Response(json, content_type="text/json")

"""XML & JSON"""
