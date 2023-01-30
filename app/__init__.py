from config.credentials import mysql_db, mysql_host, mysql_password, mysql_user
from flask import Flask
from flask_mysqldb import MySQL
from listing import listing_bp
from products import product_bp
from vending_machines import vending_bp
from vending_service import vending_service_bp

app = Flask(__name__)

app.register_blueprint(product_bp)
app.register_blueprint(vending_bp)
app.register_blueprint(listing_bp)
app.register_blueprint(vending_service_bp)

app.config["MYSQL_HOST"] = mysql_host
app.config["MYSQL_USER"] = mysql_user
app.config["MYSQL_PASSWORD"] = mysql_password
app.config["MYSQL_DB"] = mysql_db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)
