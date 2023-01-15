from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/product/delete/<int:id>')
def delete_product(id):
    pass

@app.route('/product/create/', methods=['GET', 'POST'])
def create_product():
    pass