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
    pass

@listing_bp.route('/listing/edit', methods=['POST'])
def edit_listing():
    pass

