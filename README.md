# Instrucciones

A continuación, se detallarán las instrucciones para replicar esta pequeña aplicación en su máquina local.

## Prerequisitos

Antes de ejecutar esta aplicación, debes de tener una versión actualizada de Python y MariaDB.

- Python 3.x (https://www.python.org/downloads/)
- MariaDB (https://mariadb.com/downloads/)

## Instalación de requerimientos

Para poder ejecutar el proyecto es necesario instalar los requerimientos.
Para conseguirlo ejecuta el siguiente comando en el directorio 'jewelry-database':
- pip install -r requirements.txt

## Configuración de la BD

Es necesario tener una base de datos instalada localmente para que la aplicación no muestre errores al momento de acceder a los servicios. Para esto, hay que bajar las tablas y los SP de `database.sql` en una base de datos de tu elección. Posteriormente, configura las variables de enterno del archivo `.env`. El archivo `.env.example` tiene un ejemplo de cómo deben ser llenadas.
A continuación ejecuta el siguiente comando en el directorio 'jewelry-database' para importar la bd:
- mysql -u root -p < database/database.sql

## Ejecutar la aplicación

Una vez que las dependencias hayan sido instaladas, y la base de datos haya sido configurada correctamente, el app puede ser ejecutada. Para esto, hay correr el siguiente comando dentro del folder `jewelry-database`:
- export FLASK_APP=app.py
- export FLASK_ENV_FILE=.env
- flask run --host=0.0.0.0 --port=5000

## Ejecutar microservicios

Primero, en otra terminal, dentro de la carpeta de microservicios ejecuta los siguientes comandos:
- export FLASK_APP=auth.py
- export FLASK_ENV_FILE=../.env
- flask run --host=0.0.0.0 --port=5001

Después en otra terminal, de igual manera dentro de la carpeta de microservicios ejecuta los siguientes comandos:
- export FLASK_APP=gps.py
- export FLASK_ENV_FILE=../.env
- flask run --host=0.0.0.0 --port=5002

También los siguientes comando en otra terminal
- export FLASK_APP=routes.py
- export FLASK_ENV_FILE=../.env
- flask run --host=0.0.0.0 --port=5003

Por último en una última terminal para microservicios, ejecuta las siguientes lineas
- export FLASK_APP=trucks.py
- export FLASK_ENV_FILE=../.env
- flask run --host=0.0.0.0 --port=5004

## Parar la aplicación

Para parar la aplicación presiona `Ctrl + C` en tu terminal para mandar una señal de interrupción. Para salir del ambiente virtual (en caso de haberlo creado) debes correr:

```powershell
deactivate
```