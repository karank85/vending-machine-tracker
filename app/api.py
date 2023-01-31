from typing import Any, Callable

import MySQLdb
from config.error_message import BAD_REQUEST_MESSAGE, NO_KEY_FOUND_MESSAGE
from flask import Response, jsonify, request


def import_query_run_function() -> Callable[[str], tuple[int, Any, Any]]:
    """Import run sql script function."""
    from run_query import run_sql_script

    return run_sql_script


class API:
    """API class used to handle basic api operations."""

    model_type: str

    def __init__(self, model_type: str):
        """Get model_type of the routes being used."""
        self.model_type = model_type

    @staticmethod
    def get_all_items(query_statement: str) -> Response:
        """Get all the items in the database."""
        if request.method == "GET":
            query_run_function = import_query_run_function()

            output_rows, mysql, cur = query_run_function(query_statement)

            if output_rows > 0:
                items: MySQLdb.cursors.CursorStoreResultMixIn = cur.fetchall()
                cur.close()
                return jsonify(items)
        else:
            return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)

    def get_unique_item(self, condition: str) -> Response:
        """Get a certain item from the database."""
        query_statement = f"SELECT * FROM {self.model_type} WHERE {condition}"

        query_run_function = import_query_run_function()
        if request.method == "GET":

            output_rows, mysql, cur = query_run_function(query_statement)

            if output_rows > 0:
                item: MySQLdb.cursors.CursorStoreResultMixIn = cur.fetchone()
                return jsonify(item)
            return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
        else:
            return jsonify(success=False, message=BAD_REQUEST_MESSAGE)

    def delete_item(self, query_statement: str) -> Response:
        """Delete an item from the database."""
        query_run_function = import_query_run_function()

        if request.method == "POST":

            output_rows, mysql, cur = query_run_function(query_statement)

            mysql.connection.commit()
            print(cur.fetchone())
            cur.close()
            request.method = "GET"
            return self.get_all_items(f"SELECT * FROM {self.model_type}")
        else:
            return jsonify(success=False, message=BAD_REQUEST_MESSAGE)

    def create_item(self, query_statement: str) -> Response:
        """Create a new item and adding to the database."""
        query_run_function = import_query_run_function()

        if request.method == "POST":

            output_rows, mysql, cur = query_run_function(query_statement)

            mysql.connection.commit()
            cur.close()
            request.method = "GET"
            return self.get_all_items(f"SELECT * FROM {self.model_type}")
        else:
            return jsonify(success=False, message=BAD_REQUEST_MESSAGE)

    def edit_item(self, query_statement: str, condition: str) -> Response:
        """Edit an item in the database in JSON format."""
        query_run_function = import_query_run_function()

        if request.method == "POST":

            output, mysql, cur = query_run_function(query_statement)

            mysql.connection.commit()

            if output > 0:
                cur.close()
                request.method = "GET"
                return self.get_unique_item(condition)
            else:
                return jsonify(success=False, message=NO_KEY_FOUND_MESSAGE)
        else:
            return jsonify(success=False, message=BAD_REQUEST_MESSAGE)
