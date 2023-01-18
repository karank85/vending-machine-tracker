from flask import Blueprint, request, jsonify

vending_bp = Blueprint('vending', __name__, url_prefix='/')

def import_func():
    from app import mysql
    return mysql

@vending_bp.route("/vending-machine/all", methods=['GET'])
def all_vending_machines():

    mysql = import_func()

    cur = mysql.connection.cursor()

    query_statement = f"SELECT * FROM vending_machine"
    output_rows = cur.execute(query_statement)

    if output_rows > 0:
        vending_machines = cur.fetchall()
        cur.close()
        return jsonify(vending_machines)
    return jsonify(None)

@vending_bp.route("/vending-machine", methods=['GET'])
def vending_machine():

    mysql = import_func()

    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * FROM vending_machine WHERE vending_machine_id={id}"
    output_rows = cur.execute(query_statement)
    
    if output_rows > 0:
        vm = cur.fetchone()
        return jsonify(vm)
    return None

@vending_bp.route('/vending-machine/delete')
def delete_vending_machine():

    mysql = import_func()

    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"DELETE FROM vending_machine WHERE vending_machine_id = {id}"

    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()

    return all_vending_machines()

@vending_bp.route('/vending-machine/create', methods=['GET', 'POST'])
def create_vending_machine():

    mysql = import_func()

    location = request.form['location']

    cur = mysql.connection.cursor()
    query_statement = f"INSERT INTO vending_machine(location) VALUES('{location}')"

    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()

    return all_vending_machines()

@vending_bp.route('/vending-machine/edit', methods=['POST'])
def edit_vending_machine():

    mysql = import_func()

    id = request.form['id']
    location = request.form['location']

    cur = mysql.connection.cursor()

    query_statement = f"UPDATE vending_machine SET location = '{location}' WHERE vending_machine_id={id}"
    output = cur.execute(query_statement)

    if output > 0:
        cur.close()
        return all_vending_machines()
    return jsonify(None)