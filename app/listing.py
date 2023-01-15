from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/listing/delete/<int:id>')
def delete_listing(id):
    pass

@app.route('/listing/create/', methods=['GET', 'POST'])
def create_listing():
    pass

