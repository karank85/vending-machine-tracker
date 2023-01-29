import MySQLdb
from flask import Blueprint, request, jsonify, Response

product_bp = Blueprint('product', __name__, url_prefix='/')

no_key_found_message = "no key found"
bad_request_message = "bad request"


def import_query_run_function():
    from run_query import run_sql_script
    return run_sql_script


'''
Get all the products in the database
'''


@product_bp.route("/product/all", methods=['GET'])
def all_products() -> Response:
    query_run_function = import_query_run_function()

    output_rows, mysql, cur = query_run_function(f"SELECT * FROM products")

    if output_rows > 0:
        products: MySQLdb.cursors.CursorStoreResultMixIn = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(success=False, message=no_key_found_message)


'''
Get a certain product from the datbase provided with the id
'''


@product_bp.route("/product", methods=['GET'])
def product() -> Response:
    query_run_function = import_query_run_function()
    if request.method == 'GET':
        product_id: str = request.args.get('id', type=str)

        output_rows, mysql, cur = query_run_function(f"SELECT * FROM products WHERE product_id={product_id}")

        if output_rows > 0:
            pdt: MySQLdb.cursors.CursorStoreResultMixIn = cur.fetchone()
            return jsonify(pdt)
        return jsonify(success=False, message=no_key_found_message)
    else:
        return jsonify(success=False, message=bad_request_message)


'''
Delete a product from the database
'''


@product_bp.route('/product/delete', methods=["POST"])
def delete_product() -> Response:
    query_run_function = import_query_run_function()
    if request.method == "POST":
        product_id: str = request.args.get('id', type=str)

        output_rows, mysql, cur = query_run_function(f"DELETE FROM products WHERE product_id = {product_id}")

        mysql.connection.commit()
        cur.close()
        request.method = 'GET'
        return all_products()
    else:
        return jsonify(success=False, message=bad_request_message)


'''
Create a new product and adding to the database provided
with the name and price per unit
'''


@product_bp.route('/product/create', methods=['POST'])
def create_product() -> Response:
    query_run_function = import_query_run_function()

    if request.method == 'POST':
        name: str = request.args.get('name', type=str)
        price: str = request.args.get('price', type=str)

        output_rows, mysql, cur = query_run_function(
            f"INSERT INTO products(product_name, price) VALUES('{name}',{price})")

        mysql.connection.commit()
        cur.close()
        request.method = 'GET'
        return all_products()
    else:
        return jsonify(success=False, message=bad_request_message)


'''
Lists all the listings in the database in JSON format
'''


@product_bp.route('/product/edit', methods=['POST'])
def edit_product() -> Response:
    query_run_function = import_query_run_function()
    if request.method == 'POST':
        product_id: str = request.args.get('id', type=str)
        name: str = request.args.get('name', type=str)
        price: str = request.args.get('price', type=str)
        output, mysql, cur = query_run_function(
            f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={product_id}")

        mysql.connection.commit()

        if output > 0:
            cur.close()
            request.method = 'GET'
            return product()
        else:
            return jsonify(success=False, message=no_key_found_message)
    else:
        return jsonify(success=False, message=bad_request_message)
