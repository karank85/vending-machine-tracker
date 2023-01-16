from flask import Blueprint, request, jsonify

listing_bp = Blueprint('listing', __name__, url_prefix='/')



@listing_bp.route('listing/all')
def all_listing():

    from app import mysql

    cur = mysql.connection.cursor()

    query_statement = f"SELECT * FROM listing"
    output_rows = cur.execute(query_statement)

    if output_rows > 0:
        vending_machines = cur.fetchall()
        cur.close()
        return jsonify(vending_machines)
    return jsonify(None)

@listing_bp.route("/listing", methods=['GET'])
def listing():

    from app import mysql

    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * FROM listing WHERE listing_id={id}"
    output_rows = cur.execute(query_statement)
    
    if output_rows > 0:
        ls = cur.fetchone()
        return jsonify(ls)
    return None


@listing_bp.route('/listing/delete')
def delete_listing():

    from app import mysql

    id = request.form['id']
    
    cur = mysql.connection.cursor()
    query_statement = f"DELETE FROM listing WHERE listing_id = {id}"

    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()

    return all_listing()

@listing_bp.route('/listing/create', methods=['GET', 'POST'])
def create_listing():
    
    from app import mysql

    vending_machine_id = request.form['vending_machine_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    cur = mysql.connection.cursor()
    query_statement = f"INSERT INTO listing(product_id, vending_machine_id, quantity) VALUES({product_id},{vending_machine_id},{quantity})"

    cur.execute(query_statement)
    mysql.connection.commit()

    cur.close()

    return all_listing()


@listing_bp.route('/listing/edit', methods=['POST'])
def edit_listing():
    
    from app import mysql

    id = request.form['id']
    vending_machine_id = request.form['vending_machine_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    cur = mysql.connection.cursor()
    query_statement = f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, quantity = {quantity} WHERE listing_id={id}"
    output = cur.execute(query_statement)

    if output > 0:
        cur.close()
        return listing()
    return jsonify(None)
