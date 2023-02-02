import pymysql

pymysql.install_as_MySQLdb()
from flask import Flask
from flask_mysqldb import MySQL

from app.config.credentials import mysql_db, mysql_host, mysql_password, mysql_user
from app.database import mysql
from app.routes.listing import listing_bp
from app.routes.products import product_bp
from app.routes.vending_machines import vending_bp
from app.routes.vending_service import vending_service_bp


def create_app(mysql_database: MySQL) -> Flask:
    """Start an instance of flask application."""
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

    mysql_database.init_app(app)
    return app


app_created = create_app(mysql)

if __name__ == "__main__":
    app_created.run(debug=True)
