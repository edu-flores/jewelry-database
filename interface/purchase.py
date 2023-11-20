# Flask
from flask import request, redirect, url_for
from interface import app, mysql

# Misc
import json

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
