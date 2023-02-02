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
    file = open("tests/vending_machine.sql", "r")

    for fr in file.readlines():
        output, mysql, cur = run_sql_script(fr, mysql_test_connection)


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
