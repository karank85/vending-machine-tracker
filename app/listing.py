from flask import Blueprint, request, jsonify

listing_bp = Blueprint('listing', __name__, url_prefix='/')

def import_fun():
    from util import run_sql_script
    return run_sql_script

@listing_bp.route('listing/all')
def all_listing():

    rqs = import_fun()


    output_rows, mysql, cur = rqs(f"SELECT * FROM listing")

    if output_rows > 0:
        vending_machines = cur.fetchall()
        cur.close()
        return jsonify(vending_machines)
    return jsonify(None)

@listing_bp.route("/listing", methods=['GET'])
def listing():

    rqs = import_fun()

    id = request.form['id']
    
    output_rows, mysql, cur = rqs(f"SELECT * FROM listing WHERE listing_id={id}")
    
    if output_rows > 0:
        ls = cur.fetchone()
        return jsonify(ls)
    return jsonify(None)

@listing_bp.route('/listing/buy', methods=['POST'])
def purchase_listing():

    rqs = import_fun()

    id = request.form['id']
    
    output_rows, mysql, cur = rqs(f"UPDATE listing SET quantity = quantity - 1 WHERE listing_id = {id}")

    mysql.connection.commit()
    cur.close()

    return listing()

@listing_bp.route('/listing/delete')
def delete_listing():

    rqs = import_fun()


    id = request.form['id']
    
    output_rows, mysql, cur = rqs(f"DELETE FROM listing WHERE listing_id = {id}")

    mysql.connection.commit()
    cur.close()

    return all_listing()

@listing_bp.route('/listing/create', methods=['GET', 'POST'])
def create_listing():

    rqs = import_fun()
    
    vending_machine_id = request.form['vending_machine_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    output_rows, mysql, cur = rqs(f"INSERT INTO listing(product_id, vending_machine_id, quantity) VALUES({product_id},{vending_machine_id},{quantity})")

    mysql.connection.commit()

    cur.close()

    return all_listing()


@listing_bp.route('/listing/edit', methods=['POST'])
def edit_listing():

    rqs = import_fun()
    

    id = request.form['id']
    vending_machine_id = request.form['vending_machine_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']


    output_rows, mysql, cur = rqs(f"UPDATE listing SET product_id = {product_id}, vending_machine_id = {vending_machine_id}, quantity = {quantity} WHERE listing_id={id}")


    if output_rows > 0:
        cur.close()
        return listing()
    return jsonify(None)
