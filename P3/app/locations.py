"""Locations module"""

import sqlite3
from typing import Union, Tuple
from flask import Blueprint, redirect, url_for, request, render_template
from werkzeug.wrappers import Response
from app.db import get_db
from app.auth import login_required


bp = Blueprint('locations', __name__)


@bp.route('/locations/add', methods=('GET', 'POST'))
@login_required
def add() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Add a location"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        street_num = request.form.get('street_num', '').strip()
        street_name = request.form.get('street_name', '').strip()
        city = request.form.get('city', '').strip()
        zip_code = request.form.get('zip', '').strip()
        db: sqlite3.Connection = get_db()
        db.execute(
            """
            INSERT INTO Locations (location_name, street_number, street_name, zip)
            VALUES (?, ?, ?, ?)
            """,
            (name, street_num, street_name, zip_code)
        )
        db.execute(
            """
            INSERT INTO Zip_City (zip, city)
            VALUES (?, ?)
            """,
            (zip_code, city)
        )
        db.commit()
        return redirect(url_for('browse.locations'))
    return render_template('locations/add.html')
