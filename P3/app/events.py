"""Events module for information and registration."""

import sqlite3
from datetime import datetime
from typing import Union, Tuple
from flask import Blueprint, g, redirect, url_for, flash, request, render_template
from werkzeug.wrappers import Response
from app.db import get_db
from app.auth import login_required


bp = Blueprint('events', __name__)


@bp.route('/events/<int:event_id>/signup')
@login_required
def signup(event_id: int) -> Response:
    """Sign up for an event"""
    db: sqlite3.Connection = get_db()
    try:
        db.execute(
            """
            INSERT INTO Attending (user_id, event_id)
            VALUES (?, ?)
            """,
            (g.user['user_id'], event_id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        flash('You are already signed up for this event.')
    return redirect(url_for('browse.mypage'))


@bp.route('/events/<int:event_id>/drop')
@login_required
def drop(event_id: int) -> Response:
    """Drop an event"""
    db: sqlite3.Connection = get_db()
    db.execute(
        """
        DELETE FROM Attending WHERE event_id = ? AND user_id = ?
        """,
        (event_id, g.user['user_id'])
    )
    db.commit()
    return redirect(url_for('browse.mypage'))


@bp.route('/events/<int:event_id>/reviews')
def see_review(event_id: int) -> str:
    """See the reviews on an event"""
    db: sqlite3.Connection = get_db()
    user_id = None
    if g.user:
        user_id = g.user['user_id']
    reviews = db.execute(
        """
        SELECT * 
        FROM Review NATURAL JOIN Users
        WHERE event_id = ?
        """,
        (event_id,)
    ).fetchall()
    return render_template('events/see_reviews.html', reviews=reviews, user_id=user_id)


@bp.route('/events/<int:event_id>/write_review', methods=('GET', 'POST'))
@login_required
def write_review(event_id: int) -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Write a review for an event"""
    if request.method == 'POST':
        rating = request.form.get('rating', '').strip()
        comment = request.form.get('comment', '').strip()
        if not comment:
            comment = 'N/A'
        db: sqlite3.Connection = get_db()
        db.execute(
            """
            INSERT INTO Review (user_id, event_id, rating, comment)
            VALUES (?, ?, ?, ?)
            """,
            (g.user['user_id'], event_id, rating, comment)
        )
        db.commit()
        return redirect(url_for('events.see_review', event_id=event_id))
    return render_template('events/write_review.html', event_id=event_id)


@bp.route('/events/<int:review_id>/delete_review')
@login_required
def delete_review(review_id: int) -> Response:
    """Delete a review"""
    db: sqlite3.Connection = get_db()
    review = db.execute(
        """
        SELECT event_id
        FROM Review
        WHERE review_id = ?
        """,
        (review_id,)
    ).fetchone()
    db.execute(
        """
        DELETE FROM Review WHERE review_id = ?
        """,
        (review_id,)
    )
    db.commit()
    return redirect(url_for('events.see_review', event_id=review['event_id']))


@bp.route('/events/create', methods=('GET', 'POST'))
@login_required
def create() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Create an event"""
    db: sqlite3.Connection = get_db()
    locations = db.execute(
        """
        SELECT location_name
        FROM Locations
        """,
    ).fetchall()
    groups = db.execute(
        """
        SELECT group_name
        FROM Groups
        """,
    ).fetchall()
    if request.method == 'POST':
        location = request.form.get('location', '').strip()
        name = request.form.get('name', '').strip()
        time = request.form.get('time', '').strip()
        host = request.form.get('host', '').strip()
        max_attendees = request.form.get('max_attendees', '').strip()
        if not max_attendees:
            max_attendees = '1000'
        try:
            parsed_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            flash("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS.")
            return redirect(url_for('events.create'))
        datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        db.execute(
        """
        INSERT INTO Events (location_name, event_name, time_of_day, max_attendees,
        current_attendees_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        (location, name, time, max_attendees, 0)
        )
        db.commit()
        event = db.execute(
            """
            SELECT event_id
            FROM Events
            WHERE location_name = ? AND event_name = ? AND time_of_day = ?
            """,
            (location, name, time)
        ).fetchone()
        db.execute(
        """
        INSERT INTO Hosts (group_name, event_id)
        VALUES (?, ?)
        """,
        (host, event['event_id'])
        )
        db.commit()
        return redirect(url_for('browse.events'))
    return render_template('events/create.html', groups=groups, locations=locations)


def remove_expired_events() -> Response:
    """Remove old events"""
    db: sqlite3.Connection = get_db()
    db.execute(
        """
        DELETE FROM Events
        WHERE time_of_day < ?
        """,
        (datetime.now(),)
        )
    db.commit()
    return redirect(url_for('browse.events'))
