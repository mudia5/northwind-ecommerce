import pytest
import random
import string

def generate_user_id():
    return random.randint(10000, 99999)

def generate_location_name():
    return f"TestPark{random.randint(100, 999)}"

def register_user(client, user_id):
    return client.post('/auth/register', data={
        'user_id': user_id,
        'first_name': 'Loc',
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

def test_get_add_location_form(client, app):
    with app.app_context():

        user_id = generate_user_id()
        register_response = register_user(client, user_id)
        assert register_response.status_code in (200, 302)

        login_response = login_user(client, user_id)
        assert login_response.status_code == 200
        response = client.get('/locations/add')
        assert response.status_code == 200
        assert b'Add Location' in response.data or b'location' in response.data

def test_post_add_location(client, app):
    with app.app_context():

        user_id = generate_user_id()
        register_user(client, user_id)
        login_user(client, user_id)

        location_name = generate_location_name()

        response = client.post('/locations/add', data={
            'name': location_name,
            'street_num': '123',
            'street_name': 'Main St',
            'city': 'Testville',
            'zip': '12345'
        }, follow_redirects=True)

        assert response.status_code in (200, 302)