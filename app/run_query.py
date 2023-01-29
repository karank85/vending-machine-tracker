from flask_mysqldb import MySQL
from typing import Tuple, Any

from __init__ import mysql

'''
Run sql query and execute to the database
'''


def run_sql_script(query_statement: str) -> Tuple[int, MySQL, Any]:
    cur = mysql.connection.cursor()
    output_status: int = cur.execute(query_statement)

    return output_status, mysql, cur
