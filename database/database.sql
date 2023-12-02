-- Como recomendación puedes utilizar el siguiente comando para importar la base de datos
-- completa a tu mariadb local.
-- Toma en cuenta que debes estar en el directorio raíz del proyecto:
-- mysql -u root -p < database/database.sql
-- Te pedirá ingresar tu contraseña de root con la que accedes mysql

-- Después de esto revisa que se haya importado la base de datos correctamente,
-- accediendo a mysql y entrando a la base de datos de la siguiente manera:
-- mysql -u root -p
-- 'Ingresa la contraseña con la que accedes a mysql'
-- USE jewelry;
-- SHOW TABLES;
-- Aquí revisa que esten las siguientes tablas:
-- - users
-- - trucks
-- - routes
-- - purchase_detail
-- - product
-- - purchase
-- - client
-- - address
-- - gps_data
-- - environmental_data
-- - samples
-- - short_stops
-- - long_stops
-- En caso de que existan, la base de datos se importo correctamente,
-- prosiga con las indicaciones del archivo 'README.md'

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
DROP TABLE IF EXISTS gps_data;
DROP TABLE IF EXISTS environmental_data;
DROP TABLE IF EXISTS samples;
DROP TABLE IF EXISTS short_stops;
DROP TABLE IF EXISTS long_stops;

-- Drop stored procedures if they exist
DROP PROCEDURE IF EXISTS GetPurchaseDetails;
DROP PROCEDURE IF EXISTS GetPurchaseProducts;
DROP PROCEDURE IF EXISTS CreatePurchase;
DROP PROCEDURE IF EXISTS UpdateMap;

-- Tables and sample data

CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin INT NOT NULL,
    PRIMARY KEY (user_id)
);

INSERT INTO users VALUES
(1, "Raúl", "Morales", "raul.moraless@udem.edu", "$2b$12$yBT88X2fDv8mSpE1n9jGwOSK80aE6462CBPC8azTmebFQr9fSeKnu", 0),
(2, "Edu", "Flores", "edu@a.a", "$2b$12$/hBABipOFwuzEL1GC44z2.c9aBX3py1mnoV3cFgx7Nx7crKiqv8/i", 1),
(3, "Davo", "Zavala", "a", "$2b$12$OKcFl.kRaYlFojUpp9lLHuQt06J1CGtRZbXwLjwk5nuJ/wkzHL77W", 1);

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
(3, "KFX-842", 4500, 4500, 25.6914035, -100.2513623),
(4, "GHZ-452", 6500, 5500, 25.6514035, -100.2413623),
(5, "HDW-763", 8500, 6500, 25.7414035, -100.2613623),
(6, "HVS-532", 42500, 8500, 25.7214035, -100.2713623),
(7, "DEU-346", 34500, 9500, 25.6314035, -100.3313623),
(8, "LJG-563", 15500, 7500, 25.6614035, -100.3213623),
(9, "YFZ-258", 75500, 8500, 25.6714035, -100.2813623),
(10, "FKT-975", 85500, 10500, 25.6814035, -100.2113623);

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
(1, "Ruta Común", 5500, 1, 90, 180, 1),
(2, "Route 923", 1500, 0, 60, 40, 2),
(3, "Gonzalitos", 15500, 1, 120, 320, 1),
(4, "La Peligrosa", 4500, 1, 90, 200, 3),
(5, "Consitución", 7500, 1, 100, 392, 5),
(6, "Larga", 12500, 1, 120, 853, 3),
(7, "Corta", 3500, 1, 60, 284, 6),
(8, "Norte", 28500, 1, 95, 683, 7),
(9, "Sur", 13500, 1, 78, 274, 8),
(10, "Route 392", 8400, 1, 83, 683, 9);

CREATE TABLE samples (
    sample_id INT NOT NULL AUTO_INCREMENT,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    datetime DATETIME NOT NULL,
    route_id INT NOT NULL,
    truck_id INT NOT NULL,
    distance INT NOT NULL,
    speed DOUBLE NOT NULL,
    PRIMARY KEY (sample_id)
);

INSERT INTO samples (latitude, longitude, datetime, route_id, truck_id, distance, speed)
SELECT
    RAND() * (25.8 - 25.6) + 25.6 AS latitude,
    RAND() * (-100.1 - (-100.5)) - 100.5 AS longitude,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS datetime,
    FLOOR(RAND() * 10) + 1 AS route_id,
    FLOOR(RAND() * 10) + 1 AS truck_id,
    FLOOR(RAND() * 10) + 1 AS distance,
    RAND() * 100 + 1 AS speed
FROM
    information_schema.tables t1,
    information_schema.tables t2
LIMIT 10000;

CREATE TABLE short_stops (
    short_stop_id INT NOT NULL AUTO_INCREMENT,
    route_id INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    duration INT NOT NULL,
    PRIMARY KEY (short_stop_id)
);

INSERT INTO short_stops (route_id, latitude, longitude, start_time, end_time, duration)
SELECT
    FLOOR(RAND() * 10) + 1 AS route_id,
    RAND() * (25.8 - 25.6) + 25.6 AS latitude,
    RAND() * (-100.1 - (-100.5)) - 100.5 AS longitude,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS start_time,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS end_time,
    RAND() * 100 + 1 AS duration
FROM
    information_schema.tables t1,
    information_schema.tables t2
LIMIT 10000;

CREATE TABLE long_stops (
    long_stop_id INT NOT NULL AUTO_INCREMENT,
    route_id INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    duration INT NOT NULL,
    PRIMARY KEY (long_stop_id)
);

INSERT INTO long_stops (route_id, latitude, longitude, start_time, end_time, duration)
SELECT
    FLOOR(RAND() * 10) + 1 AS route_id,
    RAND() * (25.8 - 25.6) + 25.6 AS latitude,
    RAND() * (-100.1 - (-100.5)) - 100.5 AS longitude,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS start_time,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS end_time,
    RAND() * 100 + 1 AS duration
FROM
    information_schema.tables t1,
    information_schema.tables t2
LIMIT 10000;

CREATE TABLE gps_data (
    gps_data_id INT NOT NULL AUTO_INCREMENT,
    truck_id INT NOT NULL,
    air_quality INT NOT NULL,
    contaminants INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    date DATETIME NOT NULL,
    PRIMARY KEY (gps_data_id)
);

INSERT INTO gps_data (truck_id, air_quality, contaminants, latitude, longitude, date)
SELECT
    FLOOR(RAND() * 10) + 1 AS truck_id,
    FLOOR(RAND() * 500) AS air_quality,
    FLOOR(RAND() * 2) AS contaminants,
    RAND() * (25.8 - 25.6) + 25.6 AS latitude,
    RAND() * (-100.1 - (-100.5)) - 100.5 AS longitude,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS date
FROM
    information_schema.tables t1,
    information_schema.tables t2
LIMIT 100;

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

INSERT INTO environmental_data (temperature, humidity, precipitation, wind_speed, pressure, date)
SELECT
    RAND() * (40 - 10) + 10 AS temperature,
    RAND() * 100 AS humidity,
    RAND() * 1000 AS precipitation,
    RAND() * (30 - 5) + 5 AS wind_speed,
    RAND() * (1100 - 1000) + 1000 AS pressure,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY - INTERVAL FLOOR(RAND() * 24) HOUR AS date
FROM
    information_schema.tables t1,
    information_schema.tables t2
LIMIT 10000;

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
(1, "2023-08-09 18:00:00", 1, 1, 2, "En camino", "Frida Montiel", "Me urge la entrega para mañana, es el cumpleaños de mi esposa.", 1, 12500),
(2, "2023-09-25 12:00:00", 1, 1, 2, "En camino", "Gabriel Morales", "Cuidado con el empaque.", 2, 1000),
(3, "2023-11-18 05:00:00", 1, 1, 2, "En camino", "Raúl Salinas", "Todo bien.", 3, 10500);

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
(1, "926-FH", 2, 1000),
(2, "926-FH", 1, 1000),
(3, "872-AA", 1, 10500);

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

-- Update the map shown in the interface by adding new positions in the database.
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

    -- Add sample data
    INSERT INTO samples (latitude, longitude, datetime, route_id, truck_id, distance, speed)
    SELECT latitude, longitude, NOW(), FLOOR(RAND() * 10) + 1, truck_id, FLOOR(RAND() * 10) + 1, RAND() * 100 + 1
    FROM trucks
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
END;
//

DELIMITER ;
