-- Database
DROP DATABASE IF EXISTS jewelry;
CREATE DATABASE jewelry;
USE jewelry;

-- Drop tables if they exist
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS trucks;
DROP TABLE IF EXISTS routes;
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

CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

INSERT INTO users VALUES
(1, "Raúl", "Morales", "raul.moraless@udem.edu", "666"),
(2, "Edu", "Flores", "edu@a.a", "123"),
(3, "Davo", "Zavala", "a", "a");

CREATE TABLE trucks (
    truck_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    total_distance INT NOT NULL,
    average_trip_distance INT NOT NULL,
    latitude DOUBLE,
    longitude DOUBLE,
    PRIMARY KEY (truck_id)
);

INSERT INTO trucks VALUES
(1, "SVY-312", 21000, 10000, 25.6691452, -100.3854379),
(2, "RVW-115", 1500, 1500, NULL, NULL),
(3, "KFX-842", 4500, 4500, 25.6914035, -100.2513623);

CREATE TABLE routes (
    route_id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    distance INT NOT NULL,
    active INT NOT NULL,
    average_speed INT NOT NULL,
    time INT NOT NULL,
    truck_id INT NOT NULL,
    PRIMARY KEY (route_id),
    FOREIGN KEY (truck_id) REFERENCES trucks (truck_id)
);

INSERT INTO routes VALUES
(1, "FiftyCent", 5500, 1, 90, 180, 1),
(2, "Route 923", 1500, 0, 60, 40, 2),
(3, "Gonzalitos", 15500, 1, 120, 320, 1),
(4, "La Peligrosa", 4500, 1, 90, 20, 3);

CREATE TABLE gps_data (
    gps_data_id INT NOT NULL AUTO_INCREMENT,
    truck_id INT NOT NULL,
    air_quality INT NOT NULL,
    contaminants BOOLEAN NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    date DATETIME NOT NULL,
    PRIMARY KEY (gps_data_id),
    FOREIGN KEY (truck_id) REFERENCES trucks (truck_id)
);

INSERT INTO gps_data VALUES
(1, 1, 100, TRUE, 25.6641452, -100.3851379, "2023-11-01 00:00:00"),
(2, 3, 150, TRUE, 25.6924035, -100.2533623, "2023-11-01 00:00:00"),
(3, 3, 40, FALSE, 25.6554035, -100.2563623, "2023-11-01 00:00:00"),
(4, 1, 200, TRUE, 25.6621452, -100.3857379, "2023-11-01 00:00:00");

CREATE TABLE environmental_data (
    environmental_data_id INT NOT NULL AUTO_INCREMENT,
    temperature DOUBLE,
    humidity DOUBLE,
    precipitation DOUBLE,
    wind_speed DOUBLE,
    pressure DOUBLE,
    date DATETIME NOT NULL,
    PRIMARY KEY (environmental_data_id)
);

INSERT INTO environmental_data VALUES
(1, 25.5, 55.2, 2.8, 12.1, 1012.3, "2023-11-01 00:00:00"),
(2, 26.7, 56.3, 3.1, 11.9, 1011.5, "2023-11-01 00:00:00"),
(3, 25.9, 55.7, 2.7, 12.2, 1012.1, "2023-11-01 00:00:00"),
(4, 25.2, 54.8, 2.4, 11.6, 1011.8, "2023-11-01 00:00:00"),
(5, 25.8, 56.1, 3.0, 12.0, 1012.0, "2023-11-01 00:00:00"),
(6, 25.4, 55.5, 2.6, 11.8, 1011.7, "2023-11-01 00:00:00"),
(7, 26.1, 56.4, 3.2, 12.3, 1012.2, "2023-11-01 00:00:00"),
(8, 25.6, 55.8, 2.7, 11.7, 1011.9, "2023-11-01 00:00:00"),
(9, 25.1, 54.9, 2.5, 11.5, 1011.6, "2023-11-01 00:00:00"),
(10, 25.7, 56.0, 2.9, 12.0, 1011.9, "2023-11-01 00:00:00");

CREATE TABLE address (
    address_id INT NOT NULL AUTO_INCREMENT,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    PRIMARY KEY (address_id)
);

INSERT INTO address VALUES
(1, "Club Pachuca 18", "Villa Coapa", "México", "666-666"),
(2, "Minami Josanjima-Cho Itano Gun", "Osaka-ken", "Japón", "0666");

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
    truck_id INT NOT NULL,
    total INT NOT NULL,
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (client_id) REFERENCES client (client_id),
    FOREIGN KEY (shipping_address_id) REFERENCES address (address_id),
    FOREIGN KEY (billing_address_id) REFERENCES address (address_id),
    FOREIGN KEY (truck_id) REFERENCES trucks (truck_id)
);

INSERT INTO purchase VALUES
(1, "2023-08-09 18:00:00", 1, 1, 2, "En camino", "Frida Montiel", "Me urge la entrega para mañana, es el cumpleaños de mi esposa.", 1, 12500);

CREATE TABLE product (
    product_code VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (product_code)
);

INSERT INTO product VALUES
("872-AA", "Anillo de diamante 22qt", 10500),
("926-FH", "Anillo de oro 8qt", 1000);

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
    DECLARE truck INT;

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

    -- Select a truck
    SELECT truck_id INTO truck FROM trucks WHERE latitude IS NOT NULL AND longitude IS NOT NULL ORDER BY RAND() LIMIT 1;

    -- Generate purchase general details
    INSERT INTO purchase (purchase_date, client_id, shipping_address_id, billing_address_id, status, receiver, comments, truck_id, total)
    VALUES (NOW(), client_id, shipping_address_id, billing_address_id, "En camino", receiver, comments, truck, 0);
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

CREATE PROCEDURE UpdateMap()
BEGIN
    -- Add gps data
    INSERT INTO gps_data (truck_id, air_quality, contaminants, latitude, longitude, date)
    SELECT truck_id, RAND() * 500, ROUND(RAND()), latitude, longitude, NOW()
    FROM trucks
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

    -- Move trucks
    UPDATE trucks
    SET latitude = latitude + (RAND() * 0.01 - 0.005), longitude = longitude + (RAND() * 0.01 - 0.005);
END;
//

DELIMITER ;
