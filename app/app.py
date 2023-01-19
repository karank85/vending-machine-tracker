from flask import Flask, render_template
from flask_mysqldb import MySQL
from credentials import *

app = Flask(__name__)

from products import product_bp
from vending_machines import vending_bp
from listing import listing_bp
from vending_service import vending_service_bp

app.register_blueprint(product_bp)
app.register_blueprint(vending_bp)
app.register_blueprint(listing_bp)
app.register_blueprint(vending_service_bp)

app.config['MYSQL_HOST'] = mysql_host
app.config['MYSQL_USER'] = mysql_user
app.config['MYSQL_PASSWORD'] = mysql_password
app.config['MYSQL_DB'] = mysql_db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', endpoint="home")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
