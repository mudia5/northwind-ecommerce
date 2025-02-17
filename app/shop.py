from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    return render_template('shop/index.html')
    
@bp.route('/begin')
def begin():
    return render_template('shop/begin.html')

@bp.route('/search')
def search():
    return render_template('shop/search.html')

@bp.route('/categories')
def categories():
    db = get_db()
    categories = db.execute(
        'SELECT CategoryID, CategoryName, Description FROM Categories'
    ).fetchall()
    return render_template('shop/categories.html', categories=categories)

@bp.route('/<int:categoryID>/products')
def products(categoryID):
    db = get_db()
    products = db.execute(
        'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued'
        ' FROM Products'
        ' WHERE CategoryID = ?',
        (categoryID,)
    ).fetchall()
    return render_template('shop/products.html', products=products)

@bp.route('/<int:productID>/item')
def item(productID):
    db = get_db()
    item = db.execute(
        'SELECT OrderID, UnitPrice, Quantity, Discount'
        ' FROM Order Details'
        ' WHERE ProductID = ?',
        (productID,)
    ).fetchone()
    return render_template('shop/products.html')
