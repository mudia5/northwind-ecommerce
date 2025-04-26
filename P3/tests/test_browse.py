import pytest
from tests.test_events import register_and_login

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Browse" in response.data or b"Welcome" in response.data

def test_groups_all_category(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/all/groups')
        assert response.status_code == 200
        assert b"Groups" in response.data or b"group_name" in response.data

def test_groups_specific_category(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/Music/groups')
        assert response.status_code == 200

def test_categories_page(client, app):
    with app.app_context():
        response = client.get('/categories')
        assert response.status_code == 200
        assert b"Categories" in response.data or b"category_name" in response.data

def test_locations_page(client, app):
    with app.app_context():
        response = client.get('/locations')
        assert response.status_code == 200
        assert b"Locations" in response.data or b"Zip" in response.data

def test_mypage_authenticated(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/mypage')
        assert response.status_code == 200
        assert b"My Page" in response.data or b"Account" in response.data

def test_update_mypage_get(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/mypage/update')
        assert response.status_code == 200
        assert b"Update" in response.data 

def test_update_mypage_post(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.post('/mypage/update', data={
           'first_name': 'Jane',
            'middle_initial': '',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'number': '1234567890',
            'birth_date': '1990-01-01',
            'gender': '',
            'password': 'newpassword' 
        }, follow_redirects=True)
        assert response.status_code == 200


def test_browse_events_no_filters(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/events')
        assert response.status_code == 200
        assert b"Events" in response.data or b"Browse" in response.data

def test_browse_events_invalid_category(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/events?category=invalid')
        assert response.status_code == 200
        assert b"Events" in response.data or b"No results found" in response.data


def test_browse_requires_login(client, app):
    response = client.get('/events', follow_redirects=True)
    assert b"Log In" in response.data or b"Register" in response.data

def test_browse_events_special_characters(client, app):
    with app.app_context():
        register_and_login(client, app)
        response = client.get('/events?search=%40%23%24%25')
        assert response.status_code == 200
        
