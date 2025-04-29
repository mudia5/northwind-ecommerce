"""Browse module for information pages."""

import sqlite3
from flask import Blueprint, render_template
from app.db import get_db


bp = Blueprint('browse', __name__)


@bp.route('/')
def index() -> str:
    """Render the index page"""
    return render_template('browse/index.html')


@bp.route('/groups')
def groups() -> str:
    """Render the groups page"""
    db: sqlite3.Connection = get_db()
    groups_data = db.execute(
        """
        SELECT * FROM Groups
        """
    ).fetchall()
    return render_template('groups/groups.html', groups=groups_data)


@bp.route('/categories')
def categories() -> str:
    """Render the categories page"""
    db: sqlite3.Connection = get_db()
    categories_data = db.execute(
        """
        SELECT * FROM Categories
        """
    ).fetchall()
    return render_template('browse/categories.html', categories=categories_data)


@bp.route('/events')
def events() -> str:
    """Render the events page"""
    db: sqlite3.Connection = get_db()
    events_data = db.execute(
        """
        SELECT *
        FROM Events
        """
    ).fetchall()
    attendees = db.execute(
        """
        SELECT first_name, last_name, email, event_id
        FROM Users as U, Attending as A
        WHERE U.user_id = A.user_id
        """
    ).fetchall()
    return render_template('events/events.html', events=events_data, attendees=attendees)


@bp.route('/locations')
def locations() -> str:
    """Render the locations page"""
    db: sqlite3.Connection = get_db()
    locations_data = db.execute(
        """
        SELECT *
        FROM Locations NATURAL JOIN Zip_City
        """
    ).fetchall()
    return render_template('browse/locations.html', locations=locations_data)
