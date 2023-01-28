from flask import Blueprint, request, jsonify, Response

listing_bp = Blueprint('listing', __name__, url_prefix='/')


def import_fun():
    from util import run_sql_script
    return run_sql_script


'''
Lists all the listings in the database in JSON format
'''


@listing_bp.route('listing/all')
def all_listing() -> Response:
    rqs = import_fun()

    output_rows, mysql, cur = rqs(f"SELECT * FROM listing")

    if output_rows > 0:
        vending_machines = cur.fetchall()
        cur.close()
        return jsonify(vending_machines)
    return jsonify(success=False, message="bad request")


'''
Get a listing in the database in JSON format based on the vending
machine and product 
'''


@listing_bp.route("/listing", methods=['GET'])
def listing() -> Response:
    rqs = import_fun()
    try:
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')

        output_rows, mysql, cur = rqs(
            f"SELECT * FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        if output_rows > 0:
            ls = cur.fetchone()
            return jsonify(ls)
        return jsonify(success=False, message="no key found")
    except:
        return jsonify(success=False, message="bad request")


'''
Purchase a certain listing by one
'''


@listing_bp.route('/listing/buy', methods=['POST'])
def purchase_listing() -> Response:
    rqs = import_fun()

    try:
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')

        output_rows, mysql, cur = rqs(
            f"UPDATE listing SET quantity = quantity - 1 WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()
        cur.close()

        return listing()
    except:
        return jsonify(success=False, message="bad request")


'''
Delete a listing from the database
'''


@listing_bp.route('/listing/delete')
def delete_listing() -> Response:
    rqs = import_fun()

    try:
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')

        output_rows, mysql, cur = rqs(
            f"DELETE FROM listing WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()
        cur.close()

        return all_listing()
    except:
        return jsonify(success=False, message="bad request")


'''
Create a new listing
'''


@listing_bp.route('/listing/create', methods=['GET', 'POST'])
def create_listing() -> Response:
    rqs = import_fun()
    try:
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity')

        output_rows, mysql, cur = rqs(
            f"INSERT INTO listing(product_id, vending_machine_id, quantity) VALUES({product_id},{vending_machine_id},{quantity})")

        mysql.connection.commit()

        cur.close()

        return all_listing()
    except:
        return jsonify(success=False, message="bad request")


'''
Edit a listing in the database
'''


@listing_bp.route('/listing/edit', methods=['POST'])
def edit_listing() -> Response:
    rqs = import_fun()

    try:
        vending_machine_id = request.args.get('vending_machine_id')
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity')

        output_rows, mysql, cur = rqs(
            f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, quantity = {quantity} WHERE product_id = {product_id} AND vending_machine_id = {vending_machine_id}")

        mysql.connection.commit()

        if output_rows > 0:
            cur.close()
            return listing()
        return jsonify(success=False, message="no key found")
    except:
        return jsonify(success=False, message="bad request")
