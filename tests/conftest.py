import os
import sys
import pytest
from werkzeug.security import generate_password_hash

from app.__init__ import create_app, init_db
from app.db import get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def setup_database(client, app) -> None:
    with app.app_context():
        db = get_db()
        db.execute("DELETE FROM Authentication")
        db.execute("DELETE FROM Customers")
        db.commit()

        db.execute("INSERT INTO Customers (CustomerID) VALUES ('TEST')")
        db.execute(
            "INSERT INTO Authentication (userID, password, sessionID) VALUES (?, ?, ?)", 
            ('TEST', generate_password_hash('test'), 'test_session')
        )
        db.commit()


@pytest.fixture
def app():
    db_path = "app/northwind.db"

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, user_id='TEST', password='test', headers=None):
        response = self._client.post(
            '/auth/login',
            data={'user_id': user_id, 'password': password},
            headers=headers
        )

        with self._client.session_transaction() as sess:
            sess.modified = True

        return response

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
