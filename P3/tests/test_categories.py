import pytest
import random
import string

def generate_user_id():
    return random.randint(10000, 99999)

def generate_category_name():
    return 'Cat' + ''.join(random.choices(string.ascii_uppercase, k=5))

def register_user(client, user_id):
    return client.post('/auth/register', data={
        'user_id': user_id,
        'first_name': 'Cat',
        'middle_initial': 'A',
        'last_name': 'Tester',
        'email': f'{user_id}@example.com',
        'number': '1234567890',
        'birth_date': '1990-01-01',
        'gender': 'Other',
        'password': 'testpass'
    }, follow_redirects=True)


def login_user(client, user_id):
    return client.post('/auth/login', data={
        'user_id': user_id,
        'password': 'testpass'
    }, follow_redirects=True)

def test_get_create_category_form(client, app):
    with app.app_context():
        user_id = generate_user_id()
        register_user(client, user_id)
        login_response = login_user(client, user_id)
        assert login_response.status_code == 200

        response = client.get('/categories/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'name' in response.data

def test_post_create_category(client, app):
    with app.app_context():
        user_id = generate_user_id()
        register_user(client, user_id)
        login_response = login_user(client, user_id)
        assert login_response.status_code == 200

        category_name = generate_category_name()
        response = client.post('/categories/create', data={
            'name': category_name,
            'description': 'Test category description'
        }, follow_redirects=True)

        assert response.status_code in (200, 302)
