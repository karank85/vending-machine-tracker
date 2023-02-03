import pymysql

pymysql.install_as_MySQLdb()
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app.app_run import create_app
from flask_mysqldb import MySQL
from app.util.run_query import run_sql_script

mysql_test_connection = MySQL()


def create_table():
    create_file_script = open("tests/scripts/vending_machine.sql", "r")

    for create_table_script in create_file_script.readlines():
        run_sql_script(create_table_script, mysql_test_connection)

    create_file_script.close()

    populate_data_script = open("tests/scripts/populate_data.sql", "r")

    for data_script in populate_data_script.readlines():
        run_sql_script(data_script, mysql_test_connection)


@pytest.fixture()
def app_database():
    app = create_app(mysql_test_connection)

    app.config.update(
        {
            "WTF_CSRF_CHECK_DEFAULT": False,
        }
    )

    with app.app_context():
        create_table()

    yield app, mysql_test_connection


@pytest.fixture()
def client(app_database: tuple[Flask, MySQL]) -> FlaskClient:
    app, database = app_database
    return app.test_client()
