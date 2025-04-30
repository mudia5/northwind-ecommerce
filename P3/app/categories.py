"""Categories module"""

import sqlite3
from typing import Union, Tuple
from flask import Blueprint, redirect, url_for, request, render_template
from werkzeug.wrappers import Response
from app.db import get_db
from app.auth import login_required


bp = Blueprint('categories', __name__)


@bp.route('/categories/create', methods=('GET', 'POST'))
@login_required
def create() -> Union[str, Response, Tuple[Response, int], Tuple[str, int]]:
    """Create a category"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        db: sqlite3.Connection = get_db()
        db.execute(
            """
            INSERT INTO Categories (category_name, category_description)
            VALUES (?, ?)
            """,
            (name, description)
        )
        return redirect(url_for('browse.categories'))
    return render_template('categories/create.html')
