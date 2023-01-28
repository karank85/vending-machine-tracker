from flask import Blueprint, request, jsonify, Response

product_bp = Blueprint('product', __name__, url_prefix='/')


no_key_found_message = "no key found"
bad_request_message = "bad request"

def import_fun():
    from run_query import run_sql_script
    return run_sql_script


'''
Get all the products in the database
'''


@product_bp.route("/product/all", methods=['GET'])
def all_products() -> Response:
    rqs = import_fun()
    try:
        output_rows, mysql, cur = rqs(f"SELECT * FROM products")

        if output_rows > 0:
            products = cur.fetchall()
            cur.close()
            return jsonify(products)
        return jsonify(success=False, message=no_key_found_message)
    except:
        return jsonify(success=False, message=bad_request_message)


'''
Get a certain product from the datbase provided with the id
'''


@product_bp.route("/product", methods=['GET'])
def product() -> Response:
    rqs = import_fun()
    try:
        product_id = request.args.get('id')

        output_rows, mysql, cur = rqs(f"SELECT * FROM products WHERE product_id={product_id}")

        if output_rows > 0:
            pdt = cur.fetchone()
            return jsonify(pdt)
        return jsonify(success=False, message=no_key_found_message)
    except:
        return jsonify(success=False, message=bad_request_message)


'''
Delete a product from the database
'''


@product_bp.route('/product/delete')
def delete_product() -> Response:
    rqs = import_fun()
    try:
        product_id = request.args.get('id')

        output_rows, mysql, cur = rqs(f"DELETE FROM products WHERE product_id = {product_id}")

        mysql.connection.commit()
        cur.close()

        return all_products()
    except:
        return jsonify(success=False, message=bad_request_message)


'''
Create a new product and adding to the database provided
with the name and price per unit
'''


@product_bp.route('/product/create', methods=['POST'])
def create_product() -> Response:
    rqs = import_fun()

    try:
        name = request.args.get('name')
        price = request.args.get('price')

        output_rows, mysql, cur = rqs(f"INSERT INTO products(product_name, price) VALUES('{name}',{price})")

        mysql.connection.commit()
        cur.close()

        return all_products()
    except:
        return jsonify(success=False, message=bad_request_message)


'''
Lists all the listings in the database in JSON format
'''


@product_bp.route('/product/edit', methods=['POST'])
def edit_product() -> Response:
    rqs = import_fun()
    if request.method == 'POST':
        product_id = request.args.get('id')
        name = request.args.get('name')
        price = request.args.get('price')

        (output, mysql, cur) = rqs(
            f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={product_id}")

        mysql.connection.commit()

        if output > 0:
            cur.close()
            return product()
        else:
            return jsonify(success=False, message=no_key_found_message)
    else:
        return jsonify(success=False, message=bad_request_message)
