import functools
import secrets
import string
import sqlite3
from typing import Callable, Any, Union

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import Response

from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def assign_session_id() -> None:
    if 'session_id' not in session:
        alphabet: str = string.ascii_letters
        session['session_id'] = ''.join(secrets.choice(alphabet) for _ in range(10))


@bp.route('/register', methods=('GET', 'POST'))
def register() -> Union[str, Response]:
    if request.method == 'POST':
        user_id: str = request.form['user_id'].upper()
        password: str = request.form['password']
        db: sqlite3.Connection = get_db()
        error: str | None = None

        if not user_id:
            error = 'Username is required.'
        elif len(user_id) < 5:
            error = 'Username is not long enough.'
        elif len(user_id) > 5:
            error = 'Username is too long.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    """
                    INSERT INTO Customers (CustomerID) VALUES (?)
                    """,
                    (user_id,),
                )
                db.commit()
                db.execute(
                    """
                    INSERT INTO Authentication (userID, password, sessionID) 
                    VALUES (?, ?, ?)
                    """,
                    (user_id, generate_password_hash(password), session.get('session_id')),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {user_id} is already registered.'
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login() -> Union[str, Response]:
    if request.method == 'POST':
        user_id: str = request.form['user_id'].upper()
        password: str = request.form['password']
        db: sqlite3.Connection = get_db()
        error: str | None = None
        user = db.execute(
            """
            SELECT * FROM Authentication WHERE userID = ?
            """,
            (user_id,)
        ).fetchone()
        if user is None:
            error = 'Incorrect user ID.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            url: str | None = None
            old_session_id: str = session.pop('sessionID')
            if session.get('url') is not None:
                url = session.pop('url')
            session.clear()
            session['user_id'] = user['user_id']
            session['session_id'] = user['session_id']
            session['old_session_id'] = old_session_id
            if url is not None:
                return redirect(url)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user() -> None:
    user_id: str | None = session.get('userID')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            """
            SELECT * FROM Authentication WHERE userID = ?
            """,
            (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('index'))


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(view)
    def wrapped_view(**kwargs: Any) -> Any:
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
