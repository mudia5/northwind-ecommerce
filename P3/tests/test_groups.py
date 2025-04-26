import pytest 
import random
from datetime import datetime
import uuid

def login_user(client, user_id, password='testpass'):
    return client.post('/auth/login', data={
        'user_id': user_id,
        'password': password
    }, follow_redirects=True)

def register_user(client, user_id):
    return client.post('/auth/register', data={
        'user_id': user_id,
        'first_name': 'Groupie',
        'middle_initial': 'G',
        'last_name': 'Tester',
        'email': f'{user_id}@example.com',
        'number': '1234567890',
        'birth_date': '1990-01-01',
        'gender': 'Other',
        'password': 'testpass'
    }, follow_redirects=True)

def generate_user_id():
    return random.randint(10000, 99999)

def test_create_group(client, app):
    with app.app_context():
        user_id = generate_user_id()
        register_user(client, user_id)
        login_user(client, user_id)

        response = client.post('/groups/create', data={
            'name': 'TestGroup',
            'category': 'Outdoors',
            'description': 'Test Description',
            'email': f'{user_id}@example.com',
            'website': '',
            'min_age': '',
            'max_age': '',
            'sign_up_price': ''
        }, follow_redirects=True)

        assert response.status_code == 200 or response.status_code == 302

def test_signup_and_leave_group(client, app):
    with app.app_context():
        user_id = generate_user_id()
        register_user(client, user_id)
        login_user(client, user_id)

        client.post('/groups/create', data={
            'name': 'TemporaryGroup',
            'category': 'Outdoors',
            'description': 'Test',
            'email': f'{user_id}@example.com',
            'website': '',
            'min_age': '',
            'max_age': '',
            'sign_up_price': ''
        }, follow_redirects=True)

        leave_response = client.get('/groups/TemporaryGroup/leave', follow_redirects=True)
        assert leave_response.status_code == 200


def test_signup_twice(client, app):
    with app.app_context():
        user_id = generate_user_id()
        print(f"Generated user_id: {user_id}")
        reg_response = register_user(client, user_id)
        print("Response HTML:", reg_response.data.decode())
        assert reg_response.status_code in (200, 302)

        login_response = login_user(client, user_id)
        assert login_response.status_code in (200, 302)

        group_name = 'DuplicateGroup'

        create_resp = client.post('/groups/create', data={
            'name': group_name,
            'category': 'Outdoors',
            'description': 'Duplicate test',
            'email': f'{user_id}@example.com',
            'website': '',
            'min_age': '',
            'max_age': '',
            'sign_up_price': ''
        }, follow_redirects=True)
        assert create_resp.status_code in (200, 302)

        first_signup = client.get(f'/groups/{group_name}/signup', follow_redirects=True)
        assert first_signup.status_code == 200

        second_signup = client.get(f'/groups/{group_name}/signup', follow_redirects=True)
        print("Second signup response HTML:", second_signup.data.decode())
        assert b'already signed up' in second_signup.data or b'mypage' in second_signup.data
