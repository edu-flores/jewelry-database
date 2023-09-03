from flask import Flask, Response, request, render_template
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
    return render_template("index.html", product_count=3)


@app.route("/new-purchase", methods=['POST'])
def new_purchase():
    return ""


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
        return f'<h3 style="text-align: center; margin-top: 2rem">Error - No existe una orden con el id #{id}</h3>'

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
