from flask import Blueprint, request, jsonify

vending_bp = Blueprint('vending', __name__, url_prefix='/')

def import_fun():
    from util import run_sql_script
    return run_sql_script


@vending_bp.route("/vending-machine/all", methods=['GET'])
def all_vending_machines():

    rqs = import_fun()

    output_rows, mysql, cur = rqs(f"SELECT * FROM vending_machine")

    if output_rows > 0:
        vending_machines = cur.fetchall()
        cur.close()
        return jsonify(vending_machines)
    return jsonify(None)

@vending_bp.route("/vending-machine", methods=['GET'])
def vending_machine():

    rqs = import_fun()


    id = request.form['id']
    
    output, mysql, cur = rqs(f"SELECT * FROM vending_machine WHERE vending_machine_id={id}")
    
    if output > 0:
        vm = cur.fetchone()
        return jsonify(vm)
    return None

@vending_bp.route('/vending-machine/delete')
def delete_vending_machine():

    rqs = import_fun()

    id = request.form['id']
    
    output, mysql, cur = rqs(f"DELETE FROM vending_machine WHERE vending_machine_id = {id}")

    mysql.connection.commit()
    cur.close()

    return all_vending_machines()

@vending_bp.route('/vending-machine/create', methods=['GET', 'POST'])
def create_vending_machine():

    rqs = import_fun()

    name = request.form['name']
    location = request.form['location']

    output, mysql, cur = rqs(f"INSERT INTO vending_machine(location, name) VALUES('{location}','{name}')")

    mysql.connection.commit()
    cur.close()

    return all_vending_machines()

@vending_bp.route('/vending-machine/edit', methods=['POST'])
def edit_vending_machine():

    rqs = import_fun()


    id = request.form['id']
    location = request.form['location']
    name = request.form['name']

    output, mysql ,cur = rqs(f"UPDATE vending_machine SET location = '{location}', name = '{name}' WHERE vending_machine_id={id}")

    mysql.connection.commit()

    if output > 0:
        cur.close()
        return all_vending_machines()
    return jsonify(None)