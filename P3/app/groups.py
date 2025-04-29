"""Events module for information and registration."""

from datetime import datetime, timezone
import sqlite3
from flask import Blueprint, session, redirect, url_for, flash
from app.db import get_db
from app.auth import login_required
from werkzeug.wrappers import Response


bp = Blueprint('groups', __name__)


@bp.route('/groups/<string:group_name>/signup')
@login_required
def signup(group_name: str) -> Response:
    """Render the signup page"""
    db: sqlite3.Connection = get_db()
    try:
        user_role = 'member'
        join_time = datetime.now(timezone.utc).strftime(r'%Y-%m-%d %H:%M:%S')
        db.execute(
            """
            INSERT INTO Membership (group_name, user_id, user_role, join_time, register_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (group_name, session['user_id'], user_role, join_time, join_time)
        )
        db.commit()
    except sqlite3.IntegrityError:
        flash('You are already signed up for this group.')
    return redirect(url_for('browse.groups'))
