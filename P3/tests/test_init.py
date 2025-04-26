import os
import sqlite3
import pytest
from click.testing import CliRunner
from app import init_db, create_app

def test_create_app_default_config():
    
    app = create_app()
    assert app is not None
    assert app.name == "app"
    assert app.config["SECRET_KEY"] == "dev"
    assert "auth" in app.blueprints

def test_create_app_test_config():
    
    app = create_app({'TESTING': True})
    assert app.testing is True
    assert app.config["SECRET_KEY"] == "dev"

def test_instance_folder_creation(monkeypatch, tmp_path):

    test_path = tmp_path / "instance"
    monkeypatch.setattr("os.makedirs", lambda path: None)
    app = create_app({'INSTANCE_PATH': str(test_path)})
    assert app is not None

def test_init_db_creates_schema(tmp_path, monkeypatch):

    db_path = tmp_path / "test.db"
    schema_path = tmp_path / "schema.sql"

    schema_path.write_text("""
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL
    );
    """)

    import app.__init__ as app_init
    monkeypatch.setattr(app_init, "DB_PATH", str(db_path))
    monkeypatch.setattr(app_init, "SCHEMA_PATH", str(schema_path))

    app_init.init_db()

    with sqlite3.connect(str(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';")
        assert cursor.fetchone()[0] == "test_table"

def test_init_db_command(runner):

    result = runner.invoke(args=["init-db"])
    assert "Database initialized" in result.output