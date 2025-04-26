import sqlite3
import pytest
import os
import tempfile
from app import generate_data
from unittest.mock import MagicMock


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

def test_generate_groups_raises_operational_error():
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.OperationalError("simulated failure")
    
    with pytest.raises(sqlite3.OperationalError):
        generate_data.generate_groups(mock_cursor)

def test_main_runs_without_crash(tmp_path):
    temp_db_path = tmp_path / "test_dummy.db"

    with sqlite3.connect(temp_db_path) as conn:
        cursor = conn.cursor()
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'schema.sql')
        with open(schema_path, 'r') as f:
            cursor.executescript(f.read())
        conn.commit()

    generate_data.main(str(temp_db_path))

    with sqlite3.connect(temp_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        assert 'Users' in tables

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

def test_all_generators_with_mock_cursor():
    mock_cursor = MagicMock()

    generate_data.generate_groups(mock_cursor)
    generate_data.generate_categories(mock_cursor)
    generate_data.generate_locations(mock_cursor)
    generate_data.generate_zipcity(mock_cursor)
    generate_data.generate_events(mock_cursor)
    generate_data.generate_review(mock_cursor)
    generate_data.generate_users(mock_cursor)
    generate_data.generate_userphone(mock_cursor)
    generate_data.generate_belongs(mock_cursor)
    generate_data.generate_membership(mock_cursor)
    generate_data.generate_attending(mock_cursor)
    generate_data.generate_hosts(mock_cursor)




