from __init__ import mysql 

def run_sql_script(query):

    cur = mysql.connection.cursor()
    query_statement = query
    output = cur.execute(query_statement)

    return (output,mysql,cur)
