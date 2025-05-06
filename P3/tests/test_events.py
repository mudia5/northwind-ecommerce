import pytest
import sqlite3
import random
from flask import session
from datetime import datetime, timedelta
from app.events import remove_expired_events
from app.db import get_db

def generate_user_id():
    return random.randint(10000, 99999)

def register_and_login(client, app, user_id=None, password='testpass'):
    if user_id is None:
        user_id = str(generate_user_id()) 

    with app.app_context():
        client.post('/auth/register', data={
            'user_id': user_id,
            'first_name': 'Test',
            'middle_initial': 'X',
            'last_name': 'User',
            'email': f'{user_id}@example.com',
            'number': '1234567890',
            'birth_date': '1990-01-01',
            'gender': 'Other',
            'password': password
        })

        from app.db import get_db
        db = get_db()
        user = db.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchone()
        print(f"[DEBUG] Registered user: {dict(user) if user else 'None'}")

    login_response = client.post('/auth/login', data={
        'user_id': user_id,
        'password': password
    })

    print(f"[DEBUG] Login response code: {login_response.status_code}")
    print(f"[DEBUG] Login response HTML: {login_response.data.decode()}")

    return user_id  # so you can use this in test URLs (e.g. /events/1/write_review)


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
        print("[DEBUG] Response HTML:")
        print(response.data.decode())


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

def test_write_review_invalid_rating(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.post('/events/1/write_review', data={
            'rating': '6',  # Invalid rating
            'comment': 'Nice'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Rating must be between 1 and 5' in response.data

def test_write_review_empty_comment(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.post('/events/1/write_review', data={
            'rating': '5',
            'comment': ''  # Empty comment should become 'N/A'
        }, follow_redirects=True)

        # Should redirect to see_review page (status 200), not crash
        assert response.status_code == 200
        assert b'review' in response.data or b'N/A' in response.data



def test_delete_nonexistent_review(client, app):
    with app.app_context():
        register_and_login(client, app)
        with pytest.raises(TypeError):
            client.get('/events/999/delete_review')

def test_create_event_invalid_time_format(client, app):
    with app.app_context():
        user_id = register_and_login(client, app)
        response = client.post('/events/create', data = {
            'location': 'Newton Soccer Park',
            'name': 'Invalid Time Event',
            'time': 'not-a-time',
            'host': 'The A-Team',
            'max_attendees': '100'
        }, follow_redirects=True)
        print("[DEBUG] Response HTML:")
        print(response.data.decode())

        assert b'Invalid datetime format' in response.data

def test_create_event_past_time(client, app):
    with app.app_context():
        user_id = register_and_login(client, app)
        past_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        response = client.post('/events/create', data={
            'location': 'Newton Soccer Park',
            'name': 'Past Event',
            'time': past_time,
            'host': 'The A-Team',
            'max_attendees': '100'
        }, follow_redirects=True)
        print("[DEBUG] Response HTML:")
        print(response.data.decode())

        assert b'Event time must be in the future.' in response.data

def test_remove_expired_events_runs(client, app):
    with app.app_context():
        user_id = register_and_login(client, app)

    with client:
        with client.get('/events/create'):  # trigger a request context
            response = remove_expired_events()
            assert response.status_code == 302




