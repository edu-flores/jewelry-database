-- Drop tables if they exist
DROP TABLE IF EXISTS purchase_detail;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS address;

-- Drop stored procedures if they exist
DROP PROCEDURE IF EXISTS GetPurchaseDetails;
DROP PROCEDURE IF EXISTS GetPurchaseProducts;
DROP PROCEDURE IF EXISTS CreatePurchase;

-- Tables and sample data

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
-- Get details from a purchase without its products
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

-- Get all products from a single purchase
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

-- Create a new purchase with all of its details and products
CREATE PROCEDURE CreatePurchase(
    IN first_name VARCHAR(255),
    IN last_name VARCHAR(255),
    IN email VARCHAR(255),
    IN receiver VARCHAR(255),
    IN shipping_street VARCHAR(255),
    IN shipping_city VARCHAR(255),
    IN shipping_country VARCHAR(255),
    IN shipping_postal_code VARCHAR(255),
    IN billing_street VARCHAR(255),
    IN billing_city VARCHAR(255),
    IN billing_country VARCHAR(255),
    IN billing_postal_code VARCHAR(255),
    IN comments VARCHAR(255),
    IN product_data JSON,
    OUT purchase_id INT
)
BEGIN
    DECLARE client_id INT;
    DECLARE shipping_address_id INT;
    DECLARE billing_address_id INT;
    DECLARE product_price INT;
    DECLARE total_price INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE product_code VARCHAR(255);
    DECLARE quantity INT;

    -- Create a client
    INSERT INTO client (first_name, last_name, email, password) 
    VALUES (first_name, last_name, email, "");
    SET client_id = LAST_INSERT_ID();

    -- Create shipping address
    INSERT INTO address (street, city, country, postal_code)
    VALUES (shipping_street, shipping_city, shipping_country, shipping_postal_code);
    SET shipping_address_id = LAST_INSERT_ID();

    -- Create billing address
    INSERT INTO address (street, city, country, postal_code)
    VALUES (billing_street, billing_city, billing_country, billing_postal_code);
    SET billing_address_id = LAST_INSERT_ID();

    -- Generate purchase general details
    INSERT INTO purchase (purchase_date, client_id, shipping_address_id, billing_address_id, status, receiver, comments, total)
    VALUES (NOW(), client_id, shipping_address_id, billing_address_id, "Processing", receiver, comments, 0);
    SET purchase_id = LAST_INSERT_ID();

    -- Loop through product data JSON array
    WHILE i < JSON_LENGTH(product_data) DO
        SET product_code = JSON_UNQUOTE(JSON_EXTRACT(product_data, CONCAT('$[', i, '].product_code')));
        SET quantity = JSON_UNQUOTE(JSON_EXTRACT(product_data, CONCAT('$[', i, '].quantity')));

        -- Generate purchase specific details
        SELECT price INTO product_price FROM product WHERE product_code = product_code LIMIT 1;
        INSERT INTO purchase_detail (purchase_id, product_code, quantity, subtotal)
        VALUES (purchase_id, product_code, quantity, product_price * quantity);

        SET total_price = total_price + (product_price * quantity);
        SET i = i + 1;
    END WHILE;

    -- Update total
    UPDATE purchase SET total = total_price WHERE purchase_id = purchase_id;
END;
//

DELIMITER ;