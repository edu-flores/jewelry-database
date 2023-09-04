from flask import Flask, Response, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
from lxml import etree

# Flask app
app = Flask(__name__)

app.config["MYSQL_PORT"] = 3307
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "jewelry"

mysql = MySQL(app)


# Flask routes
@app.route("/")
def home():
    msg = request.args.get("msg") or ""
    return render_template("index.html", msg=msg)


@app.route("/new-purchase", methods=['POST'])
def new_purchase():
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
    product_code = request.form.get("product_1")
    quantity = request.form.get("quantity_1")

    cursor = mysql.connection.cursor()
    cursor.callproc("CreatePurchase", (
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
        product_code,
        quantity,
        0
    ))

    # Get purchase_id
    cursor.execute("SELECT @_CreatePurchase_16")
    result = cursor.fetchone()
    purchase_id = result[0]

    mysql.connection.commit()

    return redirect(url_for("home", msg=f"Orden #{purchase_id} creada exitosamente."))


@app.route("/show-purchase/", methods=['GET'])
def show_purchase():
    id = request.args.get("id") or 0
    cursor = mysql.connection.cursor()

    # Details
    cursor.execute("CALL GetPurchaseDetails(%s)" % id)
    details = cursor.fetchall()

    # Products
    cursor.execute("CALL GetPurchaseProducts(%s)" % id)
    products = cursor.fetchall()
    
    # Error
    if not details or not products:
        return redirect(url_for("home", msg="No se encontró la orden."))

    tree = purchase_to_xml(details, products)
    xml = ET.tostring(tree.getroot(), encoding="UTF-8")

    # XSLT
    xslt = etree.parse("./static/purchase.xsl")
    transform = etree.XSLT(xslt)
    result = str(transform(etree.fromstring(xml)))

    return Response(result, content_type="text/html")


def purchase_to_xml(details, products):
    # Root element with instructions
    root = ET.Element("purchase")

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

    return ET.ElementTree(root)

# Main thread
if __name__ == "__main__":
    app.run(debug=True)
