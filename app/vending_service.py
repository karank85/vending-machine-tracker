from flask import Blueprint, request, jsonify

vending_service_bp = Blueprint('vending_service', __name__, url_prefix='/')

def import_fun():
    from util import run_sql_script
    return run_sql_script

'''
Get all the products provided by a vending machine
'''
@vending_service_bp.route('/service/machine-stock', methods=['GET'])
def vending_machine_stock():

    rqs = import_fun()

    vending_id = request.form['id']

    output_rows, mysql, cur = rqs(f"SELECT product_id, quantity FROM listing WHERE vending_machine_id = {vending_id}")

    if output_rows > 0:
        products = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(None)

'''
Lists all the listings in the database in JSON format
'''
@vending_service_bp.route('/service/location-machine', methods=['GET'])
def location_vending_machine():
    rqs = import_fun()

    location = request.form['location']

    output_rows, mysql, cur = rqs(f"SELECT vending_machine_id, name FROM vending_machine WHERE location = '{location}'")

    if output_rows > 0:
        products = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(None)


