import pytest
from flask_mysqldb import MySQL

from app.app_run import create_app

mysql_test_connection = MySQL()


@pytest.fixture()
def app_database():
    app = create_app(mysql_test_connection)
    yield app, mysql_test_connection
