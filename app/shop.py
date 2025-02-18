from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued'
                ' FROM Products'
                ' WHERE ProductName = ?',
                (name)
                # Do the string matching thing
            )
            return redirect(url_for('shop.search_results'))
    
    return render_template('shop/search.html')

@bp.route('/search-results')
def search_results():
    return render_template('shop/search_results.html')

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

@bp.route('/<int:productID>/item', methods=('GET', 'POST'))
def item(productID):
    db = get_db()
    item = db.execute(
        'SELECT OrderID, UnitPrice, Quantity, Discount'
        ' FROM "Order Details"'
        ' WHERE ProductID = ?',
        (productID,)
    ).fetchone()
    product = db.execute(
        'SELECT ProductName'
        ' FROM Products'
        ' WHERE ProductID = ?',
        (productID,)
    ).fetchone()
    
    if request.method == 'POST':
        quantity = request.form['quantity']
        error = None
        
        try:
            quantity = int(quantity)
        except ValueError:
            error = 'Input quantity contains non-numeric characters.'

        if not quantity:
            error = 'Quantity is required.'
        elif quantity > item['Quantity']:
            error = 'Quantity exceeds what is in stock.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO Shopping_Cart (shopperID, productID, quantity)'
                ' VALUES (?, ?, ?)',
                (session.get('sessionID'), productID, quantity)
                # Issue: shopperID is primary key (unique) so I cant have
                # the same person add multiple things to the cart under the same shopperID
            )
            db.commit()
            return redirect(url_for('shop.continue_shopping'))
    
    return render_template('shop/item.html', item=item, product=product) 

@bp.route('/continue')
def continue_shopping():
    return render_template('shop/continue_shop.html')
