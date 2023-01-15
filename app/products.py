from flask import Blueprint, request

product_bp = Blueprint('product', __name__, url_prefix="/")

from app import mysql

@product_bp.route("/product", methods=['GET'])
def product():
    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * FROM products WHERE product_id={id}"
    output_rows = cur.execute(query_statement)
    
    if output_rows > 0:
        pdt = cur.fetchone()
        return pdt
    return None

@product_bp.route('/product/delete')
def delete_product():
    pass

@product_bp.route('/product/create', methods=['GET', 'POST'])
def create_product():
    pass

@product_bp.route('/product/edit', methods=['POST'])
def edit_product():

    id = request.form['id']
    name = request.form['name']
    price = request.form['price']

    cur = mysql.connection.cursor()

    query_statement = f"UPDATE products SET product_name = '{name}', price = {price} WHERE product_id={id}"
    cur.execute(query_statement)
    
    return product()