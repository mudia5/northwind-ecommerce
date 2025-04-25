"""
Connect to the database
"""

import sqlite3
from datetime import datetime
from flask import current_app, g, Flask


def get_db() -> sqlite3.Connection:
    """Save the database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None) -> None:
    """Close the database connection"""
    db: sqlite3.Connection = g.pop('db', None)
    if db is not None:
        db.close()


sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app: Flask) -> None:
    """Initialize the application"""
    app.teardown_appcontext(close_db)
