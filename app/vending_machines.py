from flask import Blueprint, request, jsonify, Response

vending_bp = Blueprint('vending', __name__, url_prefix='/')


def import_fun():
    from util import run_sql_script
    return run_sql_script


'''
Lists all the vending machines in the database in JSON format
'''


@vending_bp.route("/vending-machine/all", methods=['GET'])
def all_vending_machines() -> Response:
    rqs = import_fun()

    output_rows, mysql, cur = rqs(f"SELECT * FROM vending_machine")

    if output_rows > 0:
        vending_machines = cur.fetchall()
        cur.close()
        return jsonify(vending_machines)
    return jsonify(success=False, message="bad request")


'''
Get information about a certain vending machine provided with the ID
'''


@vending_bp.route("/vending-machine", methods=['GET'])
def vending_machine() -> Response:
    rqs = import_fun()

    try:
        vending_machine_id = request.form['id']

        output, mysql, cur = rqs(f"SELECT * FROM vending_machine WHERE vending_machine_id={vending_machine_id}")

        if output > 0:
            vm = cur.fetchone()
            return jsonify(vm)
        return jsonify(success=False, message="no key found")
    except:
        return jsonify(success=False, message="bad request")


'''
Delete a vending machine from the database
'''


@vending_bp.route('/vending-machine/delete')
def delete_vending_machine() -> Response:
    rqs = import_fun()
    try:
        vending_machine_id = request.form['id']

        output, mysql, cur = rqs(f"DELETE FROM vending_machine WHERE vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()
        cur.close()

        return all_vending_machines()
    except:
        return jsonify(success=False, message="bad request")


'''
Create a new vending machine provided with the name and location
'''


@vending_bp.route('/vending-machine/create', methods=['GET', 'POST'])
def create_vending_machine() -> Response:
    rqs = import_fun()
    try:
        name = request.form['name']
        location = request.form['location']

        output, mysql, cur = rqs(f"INSERT INTO vending_machine(location, name) VALUES('{location}','{name}')")

        mysql.connection.commit()
        cur.close()
    except:
        return jsonify(success=False, message="bad request")

    return all_vending_machines()


'''
Edit the vending machine information and update it into the database
'''


@vending_bp.route('/vending-machine/edit', methods=['POST'])
def edit_vending_machine() -> Response:
    rqs = import_fun()

    try:
        vending_machine_id = request.form['id']
        location = request.form['location']
        name = request.form['name']

        output, mysql, cur = rqs(
            f"UPDATE vending_machine SET location = '{location}', name = '{name}' WHERE vending_machine_id={vending_machine_id}")

        mysql.connection.commit()

        if output > 0:
            cur.close()
            return all_vending_machines()
        return jsonify(success=False, message="no key found")
    except:
        return jsonify(success=False, message="bad request")
