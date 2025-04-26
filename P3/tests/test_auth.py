import random

def test_register_logout(client):

    unique_id = str(random.randint(10000, 99999))
    response = client.post('/auth/register', data={
        'user_id': unique_id,
        'first_name': 'Test', 
        'middle_initial': 'T',
        'last_name': 'User', 
        'email': f'{unique_id}@example.com',
        'number': '1234567890',
        'birth_date': '1995-01-01',
        'gender': 'Male',
        'password': 'testpass'
    })

    assert response.status_code == 302

def test_login_valid_user(client):
    unique_id = str(random.randint(10000, 99999))
    client.post('/auth/register', data={
        'user_id': unique_id,
        'first_name': 'Test', 
        'middle_initial': 'T',
        'last_name': 'User', 
        'email': f'{unique_id}@example.com',
        'number': '1234567890',
        'birth_date': '1995-01-01',
        'gender': 'Male',
        'password': 'testpass'
    })

    response = client.post('/auth/login', data= {
        'user_id': unique_id,
        'password': 'testpass'
    })

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')

def test_login_invalid_user(client):
    response = client.post('/auth/login', data={
        'user_id': 'wrongid',
        'password': 'wrongpass'
    }, headers={'X-TEST-MODE': '1'})

    assert response.status_code == 400
    assert b'Incorrect user ID.' in response.data or b'Incorrect password.' in response.data

def test_logout_clears_session(client):
    unique_id = str(random.randint(10000, 99999))
    client.post('/auth/register', data={
        'user_id': unique_id,
        'first_name': 'Log', 
        'middle_initial': 'O',
        'last_name': 'Out', 
        'email': f'{unique_id}@example.com',
        'number': '1234567890',
        'birth_date': '1995-01-01',
        'gender': 'Male',
        'password': 'testpass'
    })

    client.post('/auth/login', data= {
        'user_id': unique_id,
        'password': 'testpass'
    })

    response = client.get('/auth/logout')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')

