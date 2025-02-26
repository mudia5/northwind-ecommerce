from app import create_app

def test_config() -> None:
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client) -> None:
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
