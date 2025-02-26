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
    if 'session_id' not in session:
        alphabet: str = string.ascii_letters
        session['session_id'] = ''.join(secrets.choice(alphabet) for _ in range(10))


@bp.route('/register', methods=('GET', 'POST'))
def register() -> Union[str, Response, Tuple[Response, int]]:
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip().upper()
        password = request.form.get('password', '').strip()
        db = get_db()
        error = None

        print(f"DEBUG: Register attempt with user_id={user_id}, password={password}")

        if not user_id:
            return jsonify({'error': 'Username is required.'}), 400
        elif len(user_id) < 5:
            return jsonify({'error': 'Username is not long enough.'}), 400
        elif len(user_id) > 5:
            return jsonify({'error': 'Username is too long.'}), 400
        elif not password:
            return jsonify({'error': 'Password is required.'}), 400

        try:
            db.execute("INSERT INTO Customers (CustomerID) VALUES (?)", (user_id,))
            db.commit()
            db.execute("INSERT INTO Authentication (userID, password, sessionID) VALUES (?, ?, ?)",
                       (user_id, generate_password_hash(password), session.get('session_id')))
            db.commit()
        except db.IntegrityError:
            error = f'User {user_id} is already registered.'
            print(f"DEBUG: Register IntegrityError - {error}")
            return jsonify({'error': error}), 400

        print(f"DEBUG: Registration successful for {user_id}, redirecting to login.")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip().upper()
        password = request.form.get('password', '').strip()
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM Authentication WHERE userID = ?", (user_id,)).fetchone()

        print(f"DEBUG: Login attempt user_id={user_id}, password={password}")

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error:
            print(f"DEBUG: Login error - {error}")
            if request.headers.get('X-TEST-MODE'):
                return jsonify({'error': error}), 400
            flash(error)
            return render_template('auth/login.html'), 400

        session.clear()
        session['user_id'] = user['userID']
        session['session_id'] = user['sessionID']

        print(f"DEBUG: Login successful for {user_id}, redirecting to /")

        return redirect(url_for('index'))
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user() -> None:
    user_id: str | None = session.get('user_id')

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
