from typing import Tuple

import MySQLdb
from flask_mysqldb import MySQL


def run_sql_script(query_statement: str, mysql: MySQL) -> Tuple[int, MySQL, MySQLdb.cursors.Cursor]:
    """Run sql script and execute it to the database."""
    cur: MySQLdb.cursors.Cursor = mysql.connection.cursor()
    output_status: int = cur.execute(query_statement)

    return output_status, mysql, cur
