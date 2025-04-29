"""Events module for information and registration."""

import sqlite3
from flask import Blueprint, session, redirect, url_for, flash
from app.db import get_db
from app.auth import login_required
from werkzeug.wrappers import Response


bp = Blueprint('events', __name__)


@bp.route('/events/<int:event_id>/signup')
@login_required
def signup(event_id: int) -> Response:
    """Render the signup page"""
    db: sqlite3.Connection = get_db()
    try:
        db.execute(
            """
            INSERT INTO Attending (user_id, event_id)
            VALUES (?, ?)
            """,
            (session['user_id'], event_id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        flash('You are already signed up for this event.')
    return redirect(url_for('browse.events'))
