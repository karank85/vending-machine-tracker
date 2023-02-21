from flask import Response, jsonify
from flask_mysqldb import MySQL

from app.config.error_message import NO_KEY_FOUND_MESSAGE
from app.util.run_query import run_sql_script


class API:
    """API class used to handle basic api operations."""

    model_type: str
    database: MySQL

    def __init__(self, model_type: str, database: MySQL):
        """Get model_type of the routes being used."""
        self.model_type = model_type
        self.database = database

    def get_all_items(self, query_statement: str) -> tuple[Response, int]:
        """Get all the items in the database."""
        output_rows, mysql, cur = run_sql_script(query_statement, self.database)

        if output_rows > 0:
            items = cur.fetchall()
            cur.close()
            return jsonify(items), 200
        else:
            return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE), 502

    def get_unique_item(self, condition: str) -> tuple[Response, int]:
        """Get a certain item from the database."""
        query_statement = f"SELECT * FROM {self.model_type} WHERE {condition}"

        output_rows, mysql, cur = run_sql_script(query_statement, self.database)

        if output_rows > 0:
            item = cur.fetchone()
            cur.close()
            return jsonify(item), 200
        return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE), 502

    def delete_item(self, query_statement: str) -> tuple[Response, int]:
        """Delete an item from the database."""
        output_rows, mysql, cur = run_sql_script(query_statement, self.database)

        mysql.connection.commit()

        cur.close()
        return self.get_all_items(f"SELECT * FROM {self.model_type}")

    def create_item(self, query_statement: str) -> tuple[Response, int]:
        """Create a new item and adding to the database."""
        output_rows, mysql, cur = run_sql_script(query_statement, self.database)

        mysql.connection.commit()
        cur.close()
        return self.get_all_items(f"SELECT * FROM {self.model_type}")

    def edit_item(self, query_statement: str, condition: str) -> tuple[Response, int]:
        """Edit an item in the database in JSON format."""
        output, mysql, cur = run_sql_script(query_statement, self.database)

        mysql.connection.commit()

        if output > 0:
            cur.close()
            return self.get_unique_item(condition)
        else:
            return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE), 502
