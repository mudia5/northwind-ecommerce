from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from app.db import get_db
from app.auth import login_required

from datetime import datetime, timezone

bp = Blueprint('shop', __name__)


@bp.route('/')
def index():
    return render_template('shop/index.html')


@bp.route('/done')
def done():
    return render_template('shop/done.html')


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            query_name = '%' + name + '%'
            return redirect(url_for('shop.search_results', name=query_name))
    
    return render_template('shop/search.html')


@bp.route('/<string:name>/search-results')
def search_results(name):
    db = get_db()
    results = db.execute(
                'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice,'
                ' UnitsInStock, Discontinued, CategoryName'
                ' FROM Products'
                ' JOIN Categories ON Products.CategoryID = Categories.CategoryID'
                ' WHERE ProductName LIKE ? OR CategoryName LIKE ?',
                (name, name)
                ).fetchall()
    return render_template('shop/search_results.html', results=results)


@bp.route('/categories')
def categories():
    db = get_db()
    categories = db.execute(
        'SELECT CategoryID, CategoryName, Description FROM Categories'
    ).fetchall()
    return render_template('shop/categories.html', categories=categories)


@bp.route('/<int:categoryID>/<string:categoryName>/products')
def products(categoryID, categoryName):
    db = get_db()
    products = db.execute(
        'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued'
        ' FROM Products'
        ' WHERE CategoryID = ?',
        (categoryID,)
    ).fetchall()
    return render_template('shop/products.html', products=products, categoryName=categoryName)


@bp.route('/<int:productID>/item', methods=('GET', 'POST'))
def item(productID):
    db = get_db()
    item = db.execute(
        'SELECT UnitPrice, UnitsInStock, ProductName, C.CategoryID, CategoryName'
        ' FROM Products, Categories as C'
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
        elif quantity > item['UnitsInStock']:
            error = 'Quantity exceeds what is in stock.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO Shopping_Cart (shopperID, productID, quantity)'
                ' VALUES (?, ?, ?)',
                (session.get('sessionID'), productID, quantity)
            )
            db.commit()
            return redirect(url_for('shop.continue_shopping'))
    
    return render_template('shop/item.html', item=item)


@bp.route('/continue')
def continue_shopping():
    userID = session.get('userID')
    if userID is None:
        session['url'] = url_for('shop.continue_shopping')
    return render_template('shop/continue_shop.html')


def update_old_cart_items(db):
    old_sessionID = session['oldSessionID']
    db.execute(
        'UPDATE Shopping_Cart SET shopperID = ? WHERE shopperID = ?',
        (session.get('sessionID'), old_sessionID)
    )
    over_month_old = datetime.now(timezone.utc).strftime(r"%Y-%m-%d %H:%M:%S")
    db.execute(
        "DELETE FROM Shopping_Cart WHERE timestamp < datetime(?, '-30 days')",
        (over_month_old,)
    )
    db.commit()
    
    
def update_stock(db):
    cart_items = db.execute(
        'SELECT S.Quantity as RemoveQuantity, S.ProductID, P.UnitsInStock as OriginalQuantity'
        ' FROM Shopping_Cart as S, Products as P'
        ' WHERE S.ProductID = P.ProductID'
    ).fetchall()
    for remove_quantity, productID, original_quantity in cart_items:
        new_quantity = original_quantity - remove_quantity
        db.execute(
            'UPDATE Products SET UnitsInStock = ? WHERE ProductID = ?',
            (new_quantity, productID)
            )
    db.commit()
    
    
@bp.route('/clear_cart')
def clear_cart():
    db = get_db()
    db.execute(
        'DELETE FROM Shopping_Cart;'
    )
    db.commit()
    return redirect(url_for('shop.shopping_cart'))


@bp.route('/<int:productID>remove_item')
def remove_item(productID):
    db = get_db()
    db.execute(
        'DELETE FROM Shopping_Cart WHERE ProductID = ?',
        (productID,)
    )
    db.commit()
    return redirect(url_for('shop.shopping_cart'))


@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    db = get_db()
    update_old_cart_items(db)
    if request.method == 'POST':
        error = None
        orderDetails = {'Name' : request.form['name'],
                        'Address' : request.form['address'],
                        'City' : request.form['city'],
                        'Region' : request.form['region'],
                        'PostalCode' : request.form['postal_code'],
                        'Country' : request.form['country']
        }
        for key, value in orderDetails.items():
            if not value:
                error = f"{key} is required."
                
        if error is not None:
            flash(error)
        else:
            employee = db.execute(
                'SELECT EmployeeID FROM Employees WHERE (LastName, FirstName) = (?, ?)',
                ('WEB', 'WEB')
            ).fetchone()
            db.execute(
                'INSERT INTO Orders (CustomerID, EmployeeID, ShipName,'
                ' ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (session.get('userID'), employee['EmployeeID'], orderDetails['Name'],
                 orderDetails['Address'], orderDetails['City'], orderDetails['Region'],
                 orderDetails['PostalCode'], orderDetails['Country'])
            )
            update_stock(db)
            shopperID = session.get('sessionID')
            db.execute(
                'DELETE FROM Shopping_Cart WHERE shopperID = ?',
                (shopperID,)
            )
            db.commit()
            return redirect(url_for('shop.done'))
        
    return render_template('shop/checkout.html')


@bp.route('/cart', methods=('GET', 'POST'))
def shopping_cart():
    db = get_db()
    cart = db.execute(
        'SELECT S.ProductID, ProductName, Quantity, TotalPrice, UnitPrice,'
        ' (UnitPrice * Quantity) AS ItemPrice'
        ' FROM Shopping_Cart AS S, Products AS P,'
        ' (SELECT SUM(UnitPrice * Quantity) as TotalPrice'
        '     FROM Shopping_Cart AS S, Products AS P'
        '     WHERE S.ProductID = P.ProductID)'
        ' WHERE S.ProductID = P.ProductID'
        ' GROUP BY ProductName'
    ).fetchall()
    empty = True
    total = 0
    if len(cart) > 0:
        total = cart[0]['TotalPrice']
        empty = False
    
    return render_template('shop/cart.html', cart=cart, total=total, empty=empty)
