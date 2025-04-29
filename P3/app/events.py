"""Events module for information and registration."""

import sqlite3
from typing import Union, Tuple
from flask import Blueprint, g, redirect, url_for, flash, request, render_template
from app.db import get_db
from app.auth import login_required
from werkzeug.wrappers import Response


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
    return redirect(url_for('browse.events'))


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
    if g.user['user_id']:
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
