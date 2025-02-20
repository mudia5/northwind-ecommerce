import sqlite3
import os
from flask import Flask

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "northwind.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.cli.command("init-db")
    def init_db():
        try: 
            with sqlite3.connect(DB_PATH) as conn: 
                cursor = conn.cursor()
                print(f"Connected to {DB_PATH}")

                with open(SCHEMA_PATH, "r") as schema_file:
                    schema_sql = schema_file.read()
                    cursor.executescript(schema_sql)
                    print("Database schema updated successfully.")

                print(f"Database {DB_PATH} initialized successfully.")

        except Exception as e: 
            print(f"Error initializing database: {e}")

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'northwind.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import shop
    app.register_blueprint(shop.bp)
    app.add_url_rule('/', endpoint='index')

    return app