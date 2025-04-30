"""Browse module for information pages."""

import sqlite3
from typing import Union, Tuple
from flask import Blueprint, render_template, g, request, redirect, url_for
from werkzeug.wrappers import Response
from werkzeug.security import generate_password_hash
from app.db import get_db
from app.auth import login_required


bp = Blueprint('browse', __name__)


@bp.route('/')
def index() -> str:
    """Render the index page"""
    return render_template('browse/index.html')


@bp.route('/<string:category>/groups')
def groups(category) -> str:
    """Render the groups page"""
    db: sqlite3.Connection = get_db()
    user_id = None
    if g.user:
        user_id = g.user['user_id']
    if category == 'all':
        groups_data = db.execute(
            """
            SELECT * 
            FROM Groups NATURAL JOIN Belongs
            """
        ).fetchall()
    else:
        groups_data = db.execute(
            """
            SELECT * 
            FROM Groups NATURAL JOIN Belongs
            WHERE category_name = ?
            """,
            (category,)
        ).fetchall()
    user_data = db.execute(
            """
            SELECT * 
            FROM Membership
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchall()
    return render_template('groups/groups.html', groups=groups_data, user_data=user_data,
                           user_id=user_id)


@bp.route('/categories')
def categories() -> str:
    """Render the categories page"""
    db: sqlite3.Connection = get_db()
    categories_data = db.execute(
        """
        SELECT * FROM Categories
        """
    ).fetchall()
    return render_template('categories/categories.html', categories=categories_data)


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
    return render_template('locations/locations.html', locations=locations_data)


@bp.route('/mypage')
@login_required
def mypage() -> str:
    """Render the my account page"""
    db: sqlite3.Connection = get_db()
    user_id = g.user['user_id']
    groups_data = db.execute(
        """
        SELECT * 
        FROM Membership 
        WHERE user_id = ? 
        """,
        (user_id,)
    ).fetchall()
    events_data = db.execute(
        """
        SELECT *
        FROM Attending NATURAL JOIN Events
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchall()
    user_data = db.execute(
        """
        SELECT * 
        FROM Users NATURAL JOIN User_Phone
        WHERE user_id = ? 
        """,
        (user_id,)
    ).fetchone()
    if user_data is None:
        user_data = db.execute(
            """
            SELECT * 
            FROM Users
            WHERE user_id = ? 
            """,
            (user_id,)
        ).fetchone()
    return render_template('browse/mypage.html', groups=groups_data, events=events_data,
                           user_data=user_data, user_id=user_id)


@bp.route('/mypage/update', methods=('GET', 'POST'))
@login_required
def update_mypage() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Update the my account page information"""
    db: sqlite3.Connection = get_db()
    user_id = g.user['user_id']
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        middle_initial = request.form.get('middle_initial', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        number = request.form.get('number', '').strip()
        birth_date = request.form.get('birth_date', '').strip()
        gender = request.form.get('gender', '').strip()
        password = request.form.get('password', '').strip()

        if not middle_initial:
            middle_initial = 'N/A'
        if not gender:
            gender = 'N/A'
        db.execute(
                """
                UPDATE Users
                SET first_name = ?, middle_initial = ?, last_name = ?,
                email = ?, date_of_birth = ?, gender = ?, password = ?
                WHERE user_id = ?
                """,
                (first_name, middle_initial, last_name,
                    email, birth_date, gender, generate_password_hash(password), user_id)
                )
        result = db.execute(
                    """
                    SELECT * 
                    FROM Users NATURAL JOIN User_Phone
                    WHERE user_id = ? 
                    """,
                    (user_id,)
                    ).fetchone()
        if result:
            db.execute(
                    """
                    UPDATE User_Phone
                    SET phone_number = ?
                    WHERE user_id = ?
                    """,
                    (number, user_id)
                    )
        else:
            db.execute(
                    """
                    INSERT INTO User_Phone (user_id, phone_number)
                    VALUES (?, ?)
                    """,
                    (user_id, number)
                    )
        db.commit()
        return redirect(url_for('browse.mypage'))
    return render_template('browse/update.html')
