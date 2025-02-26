import pytest
from flask import session
from app.db import get_db


def test_register(client, app, setup_database) -> None:
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'user_id': 'ABCDE', 'password': 'a'}
    )

    print(f"DEBUG: Register response status = {response.status_code}")
    print(f"DEBUG: Register response headers = {response.headers}")

    assert response.status_code == 302
    assert "Location" in response.headers
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize(('user_id', 'password', 'message'), (
    ('', '', 'Username is required.'),
    ('a', '', 'Username is not long enough.'),
    ('aaaaa', '', 'Password is required.'),
    ('TEST123', 'test', 'Username is too long.')
))
def test_register_validate_input(client, user_id, password, message) -> None:
    response = client.post(
        '/auth/register',
        data={'user_id': user_id, 'password': password},
        headers={'X-TEST-MODE': '1'}
    )
    assert response.status_code == 400
    assert response.json['error'] == message


def test_login(client, auth, setup_database) -> None:
    assert client.get('/auth/login').status_code == 200

    with client.application.app_context():
        db = get_db()
        user = db.execute("SELECT * FROM Authentication WHERE userID = ?", ("ABCDE",)).fetchone()

        if user:
            db.execute("DELETE FROM Authentication WHERE userID = ?", ("ABCDE",))
            db.commit()

    register_response = client.post('/auth/register', data={'user_id': 'ABCDE', 'password': 'test'})
    print(f"DEBUG: Register response status = {register_response.status_code}")
    assert register_response.status_code == 302

    with client.application.app_context():
        db = get_db()
        user = db.execute("SELECT * FROM Authentication WHERE userID = ?", ("ABCDE",)).fetchone()
        assert user is not None, "User ABCDE was not found in the database after registration."

    response = auth.login('ABCDE', 'test')

    print(f"DEBUG: Login response status = {response.status_code}")
    print(f"DEBUG: Login response headers = {response.headers}")

    assert response.status_code == 302
    assert "Location" in response.headers
    assert response.headers["Location"] == "/"


@pytest.mark.parametrize(('user_id', 'password', 'message'), (
    ('WRONG', 'test', 'Incorrect username.'),
    ('TEST1', 'wrongpass', 'Incorrect password.'),
))
def test_login_validate_input(client, auth, setup_database, user_id, password, message) -> None:
    register_response = client.post(
        '/auth/register',
        data={'user_id': 'TEST1', 'password': 'test'},
        headers={'X-TEST-MODE': '1'}
    )

    print(f"DEBUG: Register response status = {register_response.status_code}")
    assert register_response.status_code in [200, 302]

    with client.application.app_context():
        db = get_db()
        user = db.execute("SELECT * FROM Authentication WHERE userID = ?", ("TEST1",)).fetchone()
        assert user is not None, "User TEST1 was not found in the database after registration."

    response = auth.login(user_id, password, headers={'X-TEST-MODE': '1'})

    print(f"DEBUG: Login Attempt user_id={user_id}, password={password}")
    print(f"DEBUG: Login response status = {response.status_code}")
    print(f"DEBUG: Login response JSON = {response.json}")

    assert response.status_code == 400
    assert response.json['error'] == message


def test_logout(client, auth) -> None:
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
