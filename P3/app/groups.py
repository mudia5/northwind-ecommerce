"""Events module for information and registration."""

from datetime import datetime, timezone
import sqlite3
from flask import Blueprint, g, redirect, url_for, flash
from app.db import get_db
from app.auth import login_required
from werkzeug.wrappers import Response


bp = Blueprint('groups', __name__)


@bp.route('/groups/<string:group_name>/signup')
@login_required
def signup(group_name: str) -> Response:
    """Sign up for a group"""
    db: sqlite3.Connection = get_db()
    try:
        user_role = 'member'
        join_time = datetime.now(timezone.utc).strftime(r'%Y-%m-%d %H:%M:%S')
        db.execute(
            """
            INSERT INTO Membership (group_name, user_id, user_role, join_time, register_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (group_name, g.user['user_id'], user_role, join_time, join_time)
        )
        db.commit()
    except sqlite3.IntegrityError:
        flash('You are already signed up for this group.')
    return redirect(url_for('browse.groups'))


@bp.route('/groups/<string:group_name>/drop')
@login_required
def drop(group_name: str) -> Response:
    """Drop a group"""
    db: sqlite3.Connection = get_db()
    db.execute(
        """
        DELETE FROM Membership WHERE group_name = ? AND user_id = ?
        """,
        (group_name, g.user['user_id'])
    )
    db.commit()
    return redirect(url_for('browse.mypage'))
