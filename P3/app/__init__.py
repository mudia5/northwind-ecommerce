"""
Initialization of the Flask application
"""

import sqlite3
import os
from flask import Flask

from . import db, auth, browse, events, groups, locations, categories

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
DB_PATH: str = os.path.join(BASE_DIR, 'boston_activities.db')
SCHEMA_PATH: str = os.path.join(BASE_DIR, 'schema.sql')


def init_db() -> None:
    """Initialize the database with the schema"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            print(f'Connected to {DB_PATH}')
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as schema_file:
                schema_sql: str = schema_file.read()
                cursor.executescript(schema_sql)
                print('Database schema updated successfully.')
            print(f'Database {DB_PATH} initialized successfully.')
            print('Initialized')
    except sqlite3.DatabaseError as e:
        print(f'Error initializing database: {e}')


def create_app(test_config=None) -> Flask:
    """Create and configure the Flask application"""
    app: Flask = Flask(__name__, instance_relative_config=True)
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("Database initialized")

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'boston_activities.db'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(browse.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(groups.bp)
    app.register_blueprint(locations.bp)
    app.register_blueprint(categories.bp)
    app.add_url_rule('/', endpoint='index')
    return app
