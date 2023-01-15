from flask import Flask, render_template, request, redirect, flash, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml
from products import product_bp

app = Flask(__name__)

app.register_blueprint(product_bp, url_prefix="/")

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
