import pytest
import uuid
import random
from flask import session
from datetime import datetime, timedelta

def generate_user_id():
    return random.randint(10000, 99999)

@pytest.mark.usefixtures("client")
def test_event_creation(client, app):
    with app.app_context():
        uid = generate_user_id()

        register_response = client.post('/auth/register', data={
            'user_id': uid,
            'first_name': 'Event',
            'middle_initial': 'T',
            'last_name': 'Tester',
            'email': f'{uid}@example.com',
            'number': '1234567890',
            'birth_date': '1995-01-01',
            'gender': 'Other',
            'password': 'testpass'
        }, content_type='application/x-www-form-urlencoded')

        print("Register response HTML:", register_response.data.decode())
        assert register_response.status_code in (200, 302)


        login_response = client.post('/auth/login', data={
            'user_id': uid,
            'password': 'testpass'
        })
        assert login_response.status_code in (200, 302)

        response = client.post('/events/create', data={
            'location': 'Newton Soccer Park',
            'name': 'Test Event',
            'time': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
            'host': 'The A-Team',
            'max_attendees': '100'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Test Event' in response.data or b'events' in response.data


def test_see_review(client):
    response = client.get('/events/1/reviews')
    assert response.status_code == 200
    assert b'review' in response.data or b'Great event' in response.data

def test_signup_and_drop_event(client, app):
    with app.app_context():
        client.post('/auth/login', data= {
            'user_id': '1',
            'password': 'testpass'
        })

        signup = client.get('/events/1/signup')
        assert signup.status_code == 302

        drop = client.get('/events/1/drop')
        assert drop.status_code == 302

def test_delete_review(client, app):
    with app.app_context():
        client.post('/auth/login', data={
            'user_id': '1',
            'password': 'testpass'
        })

        delete = client.get('/events/1/delete_review')
        assert delete.status_code in (302, 404)