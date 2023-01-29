import MySQLdb
from flask import Blueprint, request, jsonify, Response
from config.error_message import NO_KEY_FOUND_MESSAGE, BAD_REQUEST_MESSAGE

vending_service_bp = Blueprint('vending_service', __name__, url_prefix='/')


def import_query_run_function():
    from run_query import run_sql_script
    return run_sql_script


'''
Get all the products provided by a vending machine
'''


@vending_service_bp.route('/service/machine-stock', methods=['GET'])
def vending_machine_stock() -> Response:
    query_run_function = import_query_run_function()
    if request.method == "GET":
        vending_id: str = request.args.get('id', type=str)

        output_rows, mysql, cur = query_run_function(
            f"SELECT product_id, quantity FROM listing WHERE vending_machine_id = {vending_id}")

        if output_rows > 0:
            products: MySQLdb.CursorStoreResultMixIn = cur.fetchall()
            cur.close()
            return jsonify(products)
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)


'''
Get all the vending machines installed at a location
'''


@vending_service_bp.route('/service/location-machine', methods=['GET'])
def location_vending_machine() -> Response:
    query_run_function = import_query_run_function()
    if request.method == "GET":
        location: str = request.args.get('location', type=str)

        output_rows, mysql, cur = query_run_function(
            f"SELECT vending_machine_id, name FROM vending_machine WHERE location = '{location}'")

        if output_rows > 0:
            products: MySQLdb.CursorStoreResultMixIn = cur.fetchall()
            cur.close()
            return jsonify(products)
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
    else:
        return jsonify(success=False, message=BAD_REQUEST_MESSAGE)
