# Flask
from flask import Flask
from flask_mysqldb import MySQL

# Misc
import secrets
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

app.secret_key = secrets.token_hex(16)

# Import all other modules
from flask_app import invoice, purchase, routes, users, actions, locations
