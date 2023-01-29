from typing import Tuple

import MySQLdb.cursors
from __init__ import mysql
from flask_mysqldb import MySQL

"""
Run sql query and execute to the database
"""


def run_sql_script(query_statement: str) -> Tuple[int, MySQL, MySQLdb.cursors.Cursor]:
    """Run sql script and execute it to the database."""
    cur: MySQLdb.cursors.Cursor = mysql.connection.cursor()
    output_status: int = cur.execute(query_statement)

    return output_status, mysql, cur
