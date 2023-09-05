# Flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

# XML
import xml.etree.ElementTree as ET
from lxml import etree

# Misc
import json
from dotenv import load_dotenv
import os
load_dotenv()

# Flask main app configuration with MySQL
app = Flask(__name__)

app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

# Flask routes
@app.route("/")
def index():
    return render_template("index.html", msg=(request.args.get("msg") or ""))

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

# Create a new purchase order service
@app.route("/new-purchase", methods=["POST"])
def new_purchase():
    # Get all inputs
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    receiver = request.form.get("receiver")
    shipping_street = request.form.get("shipping_street")
    shipping_city = request.form.get("shipping_city")
    shipping_country = request.form.get("shipping_country")
    shipping_postal_code = request.form.get("shipping_postal_code")
    billing_street = request.form.get("billing_street")
    billing_city = request.form.get("billing_city")
    billing_country = request.form.get("billing_country")
    billing_postal_code = request.form.get("billing_postal_code")
    comments = request.form.get("comments")

    # Prepare product_data as a JSON object
    product_codes = request.form.getlist("product[]")
    quantities = request.form.getlist("quantity[]")
    product_data = []
    for i in range(len(product_codes)):
        product_data.append({
            "product_code": product_codes[i],
            "quantity": quantities[i]
        })
    product_data_json = json.dumps(product_data)

    # Call SP to create the purchase order
    cursor = mysql.connection.cursor()
    cursor.execute("CALL CreatePurchase(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, @purchase_id)", (
        first_name,
        last_name,
        email,
        receiver,
        shipping_street,
        shipping_city,
        shipping_country,
        shipping_postal_code,
        billing_street,
        billing_city,
        billing_country,
        billing_postal_code,
        comments,
        product_data_json
    ))

    # Get purchase_id
    cursor.execute("SELECT @purchase_id")
    result = cursor.fetchone()
    purchase_id = result[0]

    # Save changes
    mysql.connection.commit()

    return redirect(url_for("index", msg=f"Orden #{purchase_id} creada exitosamente."))

# Show a previously created purchase order with an id
@app.route("/show-purchase/<int:id>", methods=["GET"])
def show_purchase(id):
    cursor = mysql.connection.cursor()

    # Details
    cursor.execute("CALL GetPurchaseDetails(%s)" % id)
    details = cursor.fetchall()

    # Products
    cursor.execute("CALL GetPurchaseProducts(%s)" % id)
    products = cursor.fetchall()

    # Error
    if not details or not products:
        return redirect(url_for("index", msg="No se encontró la orden."))

    # Get invoice
    content = generate_xsl(id, details, products)

    return Response(content, content_type="text/html")

# Create a XML tree and transform it with XSLT
def generate_xsl(id, details, products):
    # Root element
    root = ET.Element("purchase")

    # ID
    id_element = ET.SubElement(root, "id")
    id_element.text = str(id)

    # Details
    details_element = ET.SubElement(root, "details")

    element_mapping = {
        "client": 0,
        "receiver": 1,
        "date": 2,
        "status": 3,
        "comments": 4,
        "total": -1
    }
    for element_name, index in element_mapping.items():
        element = ET.SubElement(details_element, element_name)
        element.text = str(details[0][index])

    # Addresses
    addresses_element = ET.SubElement(details_element, "addresses")

    # Shipping address
    shipping_element = ET.SubElement(addresses_element, "shipping")

    shipping_mapping = {
        "street": 5,
        "city": 6,
        "country": 7,
        "postalCode": 8
    }
    for element_name, index in shipping_mapping.items():
        element = ET.SubElement(shipping_element, element_name)
        element.text = str(details[0][index])

    # Billing address
    billing_element = ET.SubElement(addresses_element, "billing")

    billing_mapping = {
        "street": 9,
        "city": 10,
        "country": 11,
        "postalCode": 12
    }
    for element_name, index in billing_mapping.items():
        element = ET.SubElement(billing_element, element_name)
        element.text = str(details[0][index])

    # Products
    products_element = ET.SubElement(root, "products")

    for product in products:
        product_element = ET.SubElement(products_element, "product")

        product_mapping = {
            "code": 0,
            "description": 1,
            "price": 2,
            "quantity": 3,
            "subtotal": -1
        }
        for element_name, index in product_mapping.items():
            element = ET.SubElement(product_element, element_name)
            element.text = str(product[index])

    # XML
    tree = ET.ElementTree(root)
    xml = ET.tostring(tree.getroot(), encoding="UTF-8")

    # XSLT
    xslt = etree.parse("./static/purchase.xsl")
    transform = etree.XSLT(xslt)
    result = str(transform(etree.fromstring(xml)))

    return result

# Main thread
if __name__ == "__main__":
    app.run(debug=True)
