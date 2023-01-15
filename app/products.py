from flask import Blueprint, request, jsonify

product_bp = Blueprint('product', __name__, url_prefix='/')

from app import mysql

@product_bp.route("/product/all", methods=['GET'])
def all_products():
    cur = mysql.connection.cursor()

    query_statement = f"SELECT * FROM products"
    output_rows = cur.execute(query_statement)

    if output_rows > 0:
        products = cur.fetchall()
        cur.close()
        return jsonify(products)
    return jsonify(None)


@product_bp.route("/product", methods=['GET'])
def product():
    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * FROM products WHERE product_id={id}"
    output_rows = cur.execute(query_statement)
    
    if output_rows > 0:
        pdt = cur.fetchone()
        return jsonify(pdt)
    return None

@product_bp.route('/product/delete')
def delete_product():

    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"DELETE FROM products WHERE product_id = {id}"

    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()

    return all_products()

@product_bp.route('/product/create', methods=['GET', 'POST'])
def create_product():
    
    name = request.form['name']
    price = request.form['price']

    cur = mysql.connection.cursor()
    query_statement = f"INSERT INTO products(product_name, price) VALUES('{name}',{price})"

    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()

    return all_products()

@product_bp.route('/product/edit', methods=['POST'])
def edit_product():

    id = request.form['id']
    name = request.form['name']
    price = request.form['price']

    cur = mysql.connection.cursor()

    query_statement = f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={id}"
    output = cur.execute(query_statement)

    if output > 0:
        cur.close()
        return product()
    return jsonify(None)