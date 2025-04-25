from datetime import datetime, timezone
from typing import Union
import sqlite3

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.wrappers import Response

from app.db import get_db
from app.auth import login_required


bp = Blueprint('browse', __name__)


@bp.route('/')
def index() -> str:
    """Render the index page"""
    return render_template('index.html')
