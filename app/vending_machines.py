from flask import Blueprint, request, jsonify

vending_bp = Blueprint('vending', __name__, url_prefix='/')


@vending_bp.route("/vending-machine/all", methods=['GET'])
def all_vending_machines():

    from app import mysql

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

    from app import mysql

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
    pass

@vending_bp.route('/vending-machine/create', methods=['GET', 'POST'])
def create_vending_machine():
    pass

@vending_bp.route('/vending-machine/edit', methods=['POST'])
def edit_vending_machine():
    pass