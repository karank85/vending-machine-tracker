from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/vending-machine/delete/<int:id>')
def delete_vending_machine(id):
    pass

@app.route('/vending-machine/create/', methods=['GET', 'POST'])
def create_vending_machine():
    pass