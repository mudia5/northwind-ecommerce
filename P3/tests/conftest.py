import os
import tempfile
import pytest
import sqlite3 
from app import create_app
from app import generate_data



@pytest.fixture
def app(): 
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True, 
        'DATABASE': db_path,
    })

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

        schema_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'schema.sql')
        with open(schema_path, 'r') as f: 
            c.executescript(f.read())

        
        generate_data.generate_groups(c)
        generate_data.generate_categories(c)
        generate_data.generate_locations(c)
        generate_data.generate_zipcity(c)
        generate_data.generate_events(c)
        generate_data.generate_review(c)
        generate_data.generate_users(c)
        generate_data.generate_userphone(c)
        generate_data.generate_belongs(c)
        generate_data.generate_membership(c)
        generate_data.generate_attending(c)
        generate_data.generate_hosts(c)

        conn.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
