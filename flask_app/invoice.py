# Flask
from flask import Response, redirect, url_for
from flask_app import app, mysql

# XML
import xml.etree.ElementTree as ET
from lxml import etree

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
    xslt = etree.parse("./flask_app/static/html/purchase.xsl")
    transform = etree.XSLT(xslt)
    result = str(transform(etree.fromstring(xml)))

    return result
