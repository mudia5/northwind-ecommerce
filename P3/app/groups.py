"""Groups module for information and registration."""

from datetime import datetime, timezone
import sqlite3
from typing import Union, Tuple
from flask import Blueprint, g, redirect, url_for, flash, request, render_template
from werkzeug.wrappers import Response
from app.db import get_db
from app.auth import login_required


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
        flash('You have successfully signed up for this group.')
    except sqlite3.IntegrityError:
        flash('You are already signed up for this group.')
    return redirect(url_for('browse.mypage'))


@bp.route('/groups/<string:group_name>/leave')
@login_required
def leave(group_name: str) -> Response:
    """Leave a group"""
    db: sqlite3.Connection = get_db()
    db.execute(
        """
        DELETE FROM Membership WHERE group_name = ? AND user_id = ?
        """,
        (group_name, g.user['user_id'])
    )
    num_members = db.execute(
        """
        SELECT COUNT(*)
        FROM Membership
        WHERE group_name = ?
        """,
        (group_name,)
    ).fetchone()[0]
    if num_members == 0:
        db.execute(
            """
            DELETE FROM Groups WHERE group_name = ?
            """,
            (group_name,)
        )
    db.commit()
    return redirect(url_for('browse.mypage'))


@bp.route('/groups/create', methods=('GET', 'POST'))
@login_required
def create() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Create a group"""
    db: sqlite3.Connection = get_db()
    categories = db.execute(
        """
        SELECT category_name
        FROM Categories
        """,
    ).fetchall()
    if request.method == 'POST':
        group_name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        email = request.form.get('email', '').strip()
        website = request.form.get('website', '').strip()
        min_age = request.form.get('min_age', '')
        max_age = request.form.get('max_age', '')
        sign_up_price = request.form.get('sign_up_price')
        if not website:
            website = ''
        if not min_age:
            min_age = '1'
        if not max_age:
            max_age = '100'
        if not sign_up_price:
            sign_up_price = '0'
        curr_time = datetime.now(timezone.utc).strftime(r'%Y-%m-%d')
        try:
            db.execute(
                """
                INSERT INTO Groups (group_name, group_description, contact_email, website_url,
                min_age, max_age, sign_up_price, register_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (group_name, description, email, website, min_age, max_age, sign_up_price,
                curr_time)
            )
            db.execute(
                """
                INSERT INTO Belongs (group_name, category_name)
                VALUES (?, ?)
                """,
                (group_name, category)
            )
            db.execute(
                """
                INSERT INTO Membership (group_name, user_id, user_role, join_time, register_time)
                VALUES (?, ?, ?, ?, ?)
                """,
                (group_name, g.user['user_id'], 'admin', curr_time, curr_time)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash('Error creating group, try again following the style of the existing groups.')
        return redirect(url_for('browse.groups', category='all'))
    return render_template('groups/create.html', categories=categories)
