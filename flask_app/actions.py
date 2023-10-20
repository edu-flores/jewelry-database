# Flask
from flask import request, render_template, redirect, url_for
from flask_app import app, mysql

# Flask routes
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT product_code, description, price FROM product")
    products = cursor.fetchall()

    return render_template("index.html", msg=(request.args.get("msg") or ""), products=(products or ()))

# Handle form actions
@app.route("/services", methods=["POST", "GET"])
def services():
    # Create purchase
    if request.method == "POST":
        return redirect(url_for("new_purchase"))

    # Read purchase
    elif request.method == "GET":
        purchase_id = request.args.get("purchase_id", type=int)
        return redirect(url_for("show_purchase", id=purchase_id))
