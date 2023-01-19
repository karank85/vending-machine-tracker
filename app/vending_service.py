from flask import Blueprint, request, jsonify

vending_service_bp = Blueprint('vending_service', __name__, url_prefix='/')

def import_fun():
    from util import run_sql_script
    return run_sql_script

@vending_service_bp.route('/service/vending-product', methods=['GET'])
def products_from_vending_machine():

    rqs = import_fun()

    vending_id = request.form['id']

    output_rows, mysql, cur = rqs(f"SELECT product_id, quantity FROM listing WHERE vending_machine_id = {vending_id}")

    if output_rows > 0:
        products = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(None)

