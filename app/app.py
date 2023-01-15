from flask import Flask, render_template
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

from products import product_bp
from vending_machines import vending_bp

app.register_blueprint(product_bp)
app.register_blueprint(vending_bp)

cred = yaml.load(open('../cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', endpoint="home")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
