"""Authentication routes"""

import functools
import secrets
import string
from typing import Callable, Any, Union, Tuple

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import Response

from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def assign_session_id() -> None:
    """Assign a session ID to the user"""
    if 'session_id' not in session:
        alphabet: str = string.ascii_letters
        session['session_id'] = ''.join(secrets.choice(alphabet) for _ in range(10))


@bp.route('/register', methods=('GET', 'POST'))
def register() -> Union[str, Response, Tuple[Response, int]]:
    """Register a new user"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        first_name = request.form.get('first_name', '').strip()
        middle_initial = request.form.get('middle_initial', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        number = request.form.get('number', '').strip()
        birth_date = request.form.get('birth_date', '').strip()
        gender = request.form.get('gender', '').strip()
        password = request.form.get('password', '').strip()
        db = get_db()
        error = None

        if not middle_initial:
            middle_initial = 'N/A'
        if not gender:
            gender = 'N/A'

        print(f"DEBUG: Register attempt with user_id={user_id}, password={password}")

        if len(user_id) < 5:
            return jsonify({'error': 'User ID is not long enough.'}), 400
        elif len(user_id) > 5:
            return jsonify({'error': 'User ID is too long.'}), 400

        try:
            db.execute("""
                       INSERT INTO Users (user_id, first_name, middle_initial, last_name, email,
                       date_of_birth, gender, password, sessionID)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """,
                       (user_id, first_name, middle_initial, last_name,
                        email, birth_date, gender, generate_password_hash(password),
                        session.get('session_id'))
                       )
            db.execute("""
                       INSERT INTO User_Phone (user_id, phone_number)
                       VALUES (?, ?)
                       """,
                       (user_id, number)
                       )
            db.commit()
        except db.IntegrityError:
            error = f'User {user_id} is already registered.'
            print(f"DEBUG: Register IntegrityError - {error}")
            return jsonify({'error': error}), 400

        print(f"DEBUG: Registration successful for {user_id}, redirecting to login.")
        user = db.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchone()
        next_page = session.pop('next', None)
        session.clear()
        session['user_id'] = user['user_id']
        session['first_name'] = user['first_name']
        session['last_name'] = user['last_name']
        session['session_id'] = user['sessionID']
        return redirect(next_page or url_for('index'))
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Log in a user"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip().upper()
        password = request.form.get('password', '').strip()
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,)).fetchone()

        print(f"DEBUG: Login attempt user_id={user_id}, password={password}")

        if user is None:
            error = 'Incorrect user ID.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error:
            print(f"DEBUG: Login error - {error}")
            if request.headers.get('X-TEST-MODE'):
                return jsonify({'error': error}), 400
            flash(error)
            return render_template('auth/login.html'), 400

        next_page = session.pop('next', None)
        session.clear()
        session['user_id'] = user['user_id']
        session['first_name'] = user['first_name']
        session['last_name'] = user['last_name']
        session['session_id'] = user['sessionID']

        print(f"DEBUG: Login successful for {user_id}, redirecting to /")

        return redirect(next_page or url_for('index'))
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user() -> None:
    """Load the logged-in user"""
    user_id: str | None = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            """
            SELECT * FROM Users WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout() -> Response:
    """Log out the user"""
    session.clear()
    return redirect(url_for('index'))


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to ensure the user is logged in"""
    @functools.wraps(view)
    def wrapped_view(**kwargs: Any) -> Any:
        if g.user is None:
            session['next'] = request.url
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
