from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.exceptions import abort

from app.db import get_db
from app.auth import login_required

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    return render_template('shop/index.html')
    
@bp.route('/begin')
def begin():
    return render_template('shop/begin.html')

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
                'SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued'
                ' FROM Products'
                ' WHERE ProductName like ?',
                (name,)
            )
    return render_template('shop/search_results.html', results=results)

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
            )
            db.commit()
            return redirect(url_for('shop.continue_shopping'))
    
    return render_template('shop/item.html', item=item, product=product) 

@bp.route('/continue')
def continue_shopping():
    userID = session.get('userID')
    if userID is None:
        session['url'] = url_for('shop.continue_shopping')
    return render_template('shop/continue_shop.html')

@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    if request.method == 'POST':
        orderName = request.form['name']
        orderAddress = request.form['address']
        orderCity = request.form['city']
        orderRegion = request.form['region']
        orderPostalCode = request.form['postal_code']
        orderCountry = request.form['country']
        error = None
        
        orderDetails = {'Name' : orderName,
                        'Address' : orderAddress,
                        'City' : orderCity,
                        'Region' : orderRegion,
                        'PostalCode' : orderPostalCode,
                        'Country' : orderCountry
        }
        for key, value in orderDetails.items():
            if not value:
                error = f"{key} is required."
        if error is not None:
            flash(error)
        else:
            db = get_db()
            employee = db.execute(
                'SELECT EmployeeID FROM Employees WHERE (LastName, FirstName) = (?, ?)',
                ('WEB', 'WEB')
            ).fetchone()
            db.execute(
                'INSERT INTO Orders (CustomerID, EmployeeID, ShipName,'
                ' ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (session.get('userID'), employee['EmployeeID'], orderName, orderAddress,
                 orderCity, orderRegion, orderPostalCode, orderCountry)
            )
            # Remove same content from shopping cart
            # add view of shopping cart
            # need to fix the part where the same user adds to cart, logs in and gets new shopperID,
            #   then leaves and starts shopping again not logged in and with a dif shopperID
            db.execute(
                'DELETE FROM Shopping_Cart WHERE shopperID = ?',
                (session.get('shopperID'),)
            )
            db.commit()
            return redirect(url_for('shop.done'))
        
    return render_template('shop/checkout.html')
