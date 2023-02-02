import pytest
from flask import Flask
from flask.testing import FlaskClient
from app.app_run import create_app
from flask_mysqldb import MySQL

mysql_test_connection = MySQL()


@pytest.fixture()
def app_database():
    app = create_app(mysql_test_connection)
    yield app, mysql_test_connection


@pytest.fixture()
def client(app_database: tuple[Flask, MySQL]) -> FlaskClient:
    app, database = app_database
    return app.test_client()
