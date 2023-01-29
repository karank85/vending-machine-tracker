from flask import Blueprint, request, jsonify, Response

listing_bp = Blueprint('listing', __name__, url_prefix='/')


def import_query_run_function():
    from run_query import run_sql_script
    return run_sql_script


'''
Lists all the listings in the database in JSON format
'''


@listing_bp.route('listing/all', methods=['GET'])
def all_listing() -> Response:
    query_run_function = import_query_run_function()

    if request.method == 'GET':

        output_rows, mysql, cur = query_run_function(f"SELECT * FROM listing")

        if output_rows > 0:
            vending_machines = cur.fetchall()
            cur.close()
            return jsonify(vending_machines)
    else:
        return jsonify(success=False, message="bad request")


'''
Get a listing in the database in JSON format based on the vending
machine and product 
'''


@listing_bp.route("/listing", methods=['GET'])
def listing() -> Response:
    query_run_function = import_query_run_function()
    if request.method == 'GET':
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')

        output_rows, mysql, cur = query_run_function(
            f"SELECT * FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        if output_rows > 0:
            ls = cur.fetchone()
            return jsonify(ls)
        return jsonify(success=False, message="no key found")
    else:
        return jsonify(success=False, message="bad request")


'''
Purchase a certain listing by one
'''


@listing_bp.route('/listing/buy', methods=['POST'])
def purchase_listing() -> Response:
    query_run_function = import_query_run_function()

    if request.method == 'POST':
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')

        output_rows, mysql, cur = query_run_function(
            f"UPDATE listing SET quantity = quantity - 1 WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return listing()
    else:
        return jsonify(success=False, message="bad request")


'''
Delete a listing from the database
'''


@listing_bp.route('/listing/delete', methods=['POST'])
def delete_listing() -> Response:
    query_run_function = import_query_run_function()

    if request.method == 'POST':
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')

        output_rows, mysql, cur = query_run_function(
            f"DELETE FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()
        cur.close()
        request.method = "GET"
        return all_listing()
    else:
        return jsonify(success=False, message="bad request")


'''
Create a new listing
'''


@listing_bp.route('/listing/create', methods=['POST'])
def create_listing() -> Response:
    query_run_function = import_query_run_function()
    if request.method == 'POST':
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity')

        output_rows, mysql, cur = query_run_function(
            f"INSERT INTO listing(product_id, vending_machine_id, quantity) VALUES({product_id},{vending_machine_id},{quantity})")

        mysql.connection.commit()

        cur.close()
        request.method = "GET"
        return all_listing()
    else:
        return jsonify(success=False, message="bad request")


'''
Edit a listing in the database
'''


@listing_bp.route('/listing/edit', methods=['POST'])
def edit_listing() -> Response:
    query_run_function = import_query_run_function()

    if request.method == 'POST':
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity')

        output_rows, mysql, cur = query_run_function(
            f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, quantity = {quantity} WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()

        if output_rows > 0:
            cur.close()
            request.method = 'GET'
            return listing()
        return jsonify(success=False, message="no key found")
    else:
        return jsonify(success=False, message="bad request")
