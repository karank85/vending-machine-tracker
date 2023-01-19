from flask import Blueprint, request, jsonify

product_bp = Blueprint('product', __name__, url_prefix='/')

def import_fun():
    from util import run_sql_script
    return run_sql_script


@product_bp.route("/product/all", methods=['GET'])
def all_products():

    rqs = import_fun()

    output_rows, mysql, cur = rqs(f"SELECT * FROM products")

    if output_rows > 0:
        products = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(None)


@product_bp.route("/product", methods=['GET'])
def product():

    rqs = import_fun()

    id = request.form['id']
    
    output_rows, mysql, cur = rqs(f"SELECT * FROM products WHERE product_id={id}")
    
    if output_rows > 0:
        pdt = cur.fetchone()
        return jsonify(pdt)
    return jsonify(None)

@product_bp.route('/product/delete')
def delete_product():

    rqs = import_fun()

    id = request.form['id']
    
    output_rows, mysql, cur = rqs(f"DELETE FROM products WHERE product_id = {id}")

    mysql.connection.commit()
    cur.close()

    return all_products()

@product_bp.route('/product/create', methods=['GET', 'POST'])
def create_product():

    rqs = import_fun()
    
    name = request.form['name']
    price = request.form['price']

    output_rows, mysql, cur = rqs(f"INSERT INTO products(product_name, price) VALUES('{name}',{price})")

    mysql.connection.commit()
    cur.close()

    return all_products()

@product_bp.route('/product/edit', methods=['POST'])
def edit_product():

    rqs = import_fun()

    id = request.form['id']
    name = request.form['name']
    price = request.form['price']

    (output, mysql, cur) = rqs(f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={id}")

    mysql.connection.commit()

    if output > 0:
        cur.close()
        return product()
    return jsonify(None)