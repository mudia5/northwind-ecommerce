import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

import secrets, string


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def assign_sessionID():
    if 'sessionID' not in session:
        alphabet = string.ascii_letters
        session['sessionID'] = ''.join(secrets.choice(alphabet) for _ in range(10))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        userID = request.form['userID'].upper()
        password = request.form['password']
        db = get_db()
        error = None

        if not userID:
            error = 'Username is required.'
        elif len(userID) < 5:
            error = 'Username is not long enough.'
        elif len(userID) > 5:
            error = 'Username is too long.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Customers (CustomerID) VALUES (?)",
                    (userID,),
                )
                db.commit()
                db.execute(
                    "INSERT INTO Authentication (userID, password, sessionID) VALUES (?, ?, ?)",
                    (userID, generate_password_hash(password), session.get('sessionID')),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {userID} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        userID = request.form['userID'].upper()
        password = request.form['password']
        db = get_db()
        error = None
        # db.execute(
        #     "UPDATE Authentication SET sessionID = ?",
        #     (session.get('sessionID'),)
        # )
        # db.commit()
        user = db.execute(
            'SELECT * FROM Authentication WHERE userID = ?', (userID,)
        ).fetchone()
        if user is None:
            error = 'Incorrect userID.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session.clear()
            session['userID'] = user['userID']
            session['sessionID'] = user['sessionID']
            redirect_url = session.pop('url', None)
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    userID = session.get('userID')

    if userID is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Authentication WHERE userID = ?', (userID,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view