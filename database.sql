-- Tables and Data

CREATE TABLE address (
    address_id INT NOT NULL AUTO_INCREMENT,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    PRIMARY KEY (address_id)
);

INSERT INTO address VALUES
(1, "Club Pachuca 18", "Villa Coapa", "Mexico", "666-666"),
(2, "Minami Josanjima-Cho Itano Gun", "Osaka-ken", "Japan", "0666");

CREATE TABLE client (
    client_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (client_id)
);

INSERT INTO client VALUES
(1, "Raúl", "Morales", "raul.moraless@udem.edu", "666");

CREATE TABLE purchase (
    purchase_id INT NOT NULL AUTO_INCREMENT,
    purchase_date DATETIME NOT NULL,
    client_id INT NOT NULL,
    shipping_address_id INT NOT NULL,
    billing_address_id INT NOT NULL,
    status VARCHAR(255) NOT NULL,
    receiver VARCHAR(255) NOT NULL,
    comments VARCHAR(255),
    total INT NOT NULL,
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (client_id) REFERENCES client (client_id),
    FOREIGN KEY (shipping_address_id) REFERENCES address (address_id),
    FOREIGN KEY (billing_address_id) REFERENCES address (address_id)
);

INSERT INTO purchase VALUES
(1, "2023-08-09 18:00:00", 1, 1, 2, "Processing", "Frida Montiel", "Me urge la entrega para mañana, es el cumpleaños de mi esposa.", 12500);

CREATE TABLE product (
    product_code VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (product_code)
);

INSERT INTO product VALUES
("872-AA", "Diamond ring 22ct", 10500),
("926-FH", "Golden ring 8ct", 1000);

CREATE TABLE purchase_detail (
    purchase_id INT NOT NULL,
    product_code VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    subtotal INT NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchase (purchase_id),
    FOREIGN KEY (product_code) REFERENCES product (product_code)
);

INSERT INTO purchase_detail VALUES
(1, "872-AA", 1, 10500),
(1, "926-FH", 2, 2000);

-- Stored Procedures

DELIMITER //
CREATE PROCEDURE GetPurchaseDetails(IN id INT)
BEGIN
    SELECT 
        CONCAT(client.first_name, " ", client.last_name) AS client,
        purchase.receiver,
        purchase.purchase_date,
        purchase.status,
        purchase.comments,
        address_shipping.street AS shipping_street,
        address_shipping.city AS shipping_city,
        address_shipping.country AS shipping_country,
        address_shipping.postal_code AS shipping_postal_code,
        address_billing.street AS billing_street,
        address_billing.city AS billing_city,
        address_billing.country AS billing_country,
        address_billing.postal_code AS billing_postal_code,
        purchase.total
    FROM purchase
    INNER JOIN purchase_detail ON purchase.purchase_id = purchase_detail.purchase_id
    INNER JOIN client ON purchase.client_id = client.client_id
    INNER JOIN address AS address_shipping ON purchase.shipping_address_id = address_shipping.address_id
    INNER JOIN address AS address_billing ON purchase.billing_address_id = address_billing.address_id
    WHERE purchase.purchase_id = id;
END;

CREATE PROCEDURE GetPurchaseProducts(IN id INT)
BEGIN
    SELECT 
        product.product_code,
        product.description,
        product.price,
        purchase_detail.quantity,
        purchase_detail.subtotal
    FROM purchase
    INNER JOIN purchase_detail ON purchase.purchase_id = purchase_detail.purchase_id
    INNER JOIN product ON purchase_detail.product_code = product.product_code
    WHERE purchase.purchase_id = id;
END;
//

DELIMITER ;