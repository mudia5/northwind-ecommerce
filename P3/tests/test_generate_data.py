import sqlite3
import pytest
import os
from app import generate_data
from unittest.mock import MagicMock

"""
def test_generate_groups_error_handling():
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.OperationalError("Mock error")

    try:
        generate_data.generate_groups(mock_cursor)
    except sqlite3.OperationalError as e:
        assert str(e) == "Mock error"
"""

@pytest.fixture(scope="function")
def db_cursor():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'schema.sql')
    with open(schema_path, 'r') as f:
        cursor.executescript(f.read())

    yield cursor

    conn.commit()
    conn.close()

def test_generate_groups(db_cursor):
    generate_data.generate_groups(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Groups").fetchone()[0]
    assert result == 2

def test_generate_categories(db_cursor):
    generate_data.generate_categories(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Categories").fetchone()[0]
    assert result == 7

def test_generate_locations(db_cursor):
    generate_data.generate_locations(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Locations").fetchone()[0]
    assert result == 7

def test_generate_zipcity(db_cursor):
    generate_data.generate_zipcity(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Zip_City").fetchone()[0]
    assert result == 7

def test_generate_events(db_cursor):
    generate_data.generate_locations(db_cursor)
    generate_data.generate_events(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Events").fetchone()[0]
    assert result == 2

def test_generate_review(db_cursor):
    generate_data.generate_users(db_cursor)
    generate_data.generate_locations(db_cursor)
    generate_data.generate_events(db_cursor)
    generate_data.generate_review(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Review").fetchone()[0]
    assert result == 2

def test_generate_users(db_cursor):
    generate_data.generate_users(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0]
    assert result == 20

def test_generate_userphone(db_cursor):
    generate_data.generate_users(db_cursor)
    generate_data.generate_userphone(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM User_Phone").fetchone()[0]
    assert result == 21

def test_generate_belongs(db_cursor):
    generate_data.generate_groups(db_cursor)
    generate_data.generate_categories(db_cursor)
    generate_data.generate_belongs(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Belongs").fetchone()[0]
    assert result == 2

def test_generate_membership(db_cursor):
    generate_data.generate_users(db_cursor)
    generate_data.generate_groups(db_cursor)
    generate_data.generate_membership(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Membership").fetchone()[0]
    assert result == 21

def test_generate_attending(db_cursor):
    generate_data.generate_users(db_cursor)
    generate_data.generate_locations(db_cursor)
    generate_data.generate_events(db_cursor)
    generate_data.generate_attending(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Attending").fetchone()[0]
    assert result == 21

def test_generate_hosts(db_cursor):
    generate_data.generate_groups(db_cursor)
    generate_data.generate_locations(db_cursor)
    generate_data.generate_events(db_cursor)
    generate_data.generate_hosts(db_cursor)
    result = db_cursor.execute("SELECT COUNT(*) FROM Hosts").fetchone()[0]
    assert result == 2


'''
def test_main(monkeypatch):
    original_connect = sqlite3.connect
    shared_conn = original_connect(":memory:")

    def mock_connect(path):
        print(f"mock_connect called with: {path}")
        return shared_conn
    
    def mock_close():
        print("mock close ignored")
    
    monkeypatch.setattr(sqlite3, "connect", mock_connect)
    monkeypatch.setattr(shared_conn, "close", mock_close)


    schema_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'schema.sql')
    with open(schema_path, 'r') as f:
        shared_conn.executescript(f.read())
    shared_conn.commit()

    generate_data.main()

    cursor = shared_conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM Groups").fetchone()[0]
    assert count == 2
'''



