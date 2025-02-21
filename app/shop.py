from datetime import datetime, timezone
from typing import Union
import sqlite3

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.wrappers import Response

from app.db import get_db
from app.auth import login_required


bp = Blueprint('shop', __name__)


@bp.route('/')
def index() -> str:
    return render_template('shop/index.html')


@bp.route('/done')
def done() -> str:
    return render_template('shop/done.html')


@bp.route('/search', methods=('GET', 'POST'))
def search() -> Union[str, Response]:
    if request.method == 'POST':
        name: str = request.form['name']
        error: str | None = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            query_name: str = '%' + name + '%'
            return redirect(url_for('shop.search_results', name=query_name))

    return render_template('shop/search.html')


@bp.route('/<string:name>/search-results')
def search_results(name: str) -> str:
    db: sqlite3.Connection = get_db()
    product_search_results = db.execute(
                """
                SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, 
                UnitsInStock, Discontinued, CategoryName'
                FROM Products'
                JOIN Categories ON Products.CategoryID = Categories.CategoryID'
                WHERE ProductName LIKE ? OR CategoryName LIKE ?
                """,
                (name, name)
                ).fetchall()
    return render_template('shop/search_results.html', results=product_search_results)


@bp.route('/categories')
def categories() -> str:
    db: sqlite3.Connection = get_db()
    product_categories = db.execute(
        """
        SELECT CategoryID, CategoryName, Description 
        FROM Categories
        """
    ).fetchall()
    return render_template('shop/categories.html', categories=product_categories)


@bp.route('/<int:category_id>/products')
def products(category_id) -> str:
    db: sqlite3.Connection = get_db()
    product_details = db.execute(
        """
        SELECT ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, 
        Discontinued, CategoryName
        FROM Products, Categories 
        WHERE Products.CategoryID = ? and Categories.CategoryID = ?
        """,
        (category_id, category_id)
    ).fetchall()
    return render_template('shop/products.html', products=product_details)


@bp.route('/<int:product_id>/item', methods=('GET', 'POST'))
def item(product_id) -> Union[str, Response]:
    db: sqlite3.Connection = get_db()
    item_details = db.execute(
        """
        SELECT UnitPrice, UnitsInStock, ProductName, C.CategoryID, CategoryName 
        FROM Products, Categories as C 
        WHERE ProductID = ?
        """,
        (product_id,)
    ).fetchone()

    if request.method == 'POST':
        quantity: str | int = request.form['quantity']
        error: str | None = None

        try:
            quantity = int(quantity)
        except ValueError:
            error = 'Input quantity contains non-numeric characters.'

        if not quantity:
            error = 'Quantity is required.'
        elif quantity > item_details['UnitsInStock']:
            error = 'Quantity exceeds what is in stock.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                """
                INSERT INTO Shopping_Cart (shopperID, productID, quantity) 
                VALUES (?, ?, ?)
                """,
                (session.get('session_id'), product_id, quantity)
            )
            db.commit()
            return redirect(url_for('shop.continue_shopping'))

    return render_template('shop/item.html', item=item_details)


@bp.route('/continue')
def continue_shopping() -> Union[str, Response]:
    user_id: str | None = session.get('user_id')
    if user_id is None:
        session['url'] = url_for('shop.continue_shopping')
    return render_template('shop/continue_shop.html')


def update_old_cart_items(db: sqlite3.Connection) -> None:
    old_session_id: str = session['old_session_id']
    db.execute(
        """
        UPDATE Shopping_Cart SET shopperID = ? WHERE shopperID = ?
        """,
        (session.get('session_id'), old_session_id)
    )
    over_month_old: str = datetime.now(timezone.utc).strftime(r'%Y-%m-%d %H:%M:%S')
    db.execute(
        """
        DELETE FROM Shopping_Cart WHERE timestamp < datetime(?, '-30 days')
        """,
        (over_month_old,)
    )
    db.commit()


def update_stock(db: sqlite3.Connection) -> None:
    cart_items = db.execute(
        """
        SELECT S.Quantity as RemoveQuantity, S.ProductID, P.UnitsInStock as OriginalQuantity 
        FROM Shopping_Cart as S, Products as P 
        WHERE S.ProductID = P.ProductID
        """
    ).fetchall()
    for remove_quantity, product_id, original_quantity in cart_items:
        new_quantity: int = original_quantity - remove_quantity
        db.execute(
            """
            UPDATE Products SET UnitsInStock = ? WHERE ProductID = ?
            """,
            (new_quantity, product_id)
            )
    db.commit()


@bp.route('/clear_cart')
def clear_cart() -> Response:
    db: sqlite3.Connection = get_db()
    db.execute(
        """
        DELETE FROM Shopping_Cart
        """
    )
    db.commit()
    return redirect(url_for('shop.shopping_cart'))


@bp.route('/<int:product_id>remove_item')
def remove_item(product_id: int) -> Response:
    db: sqlite3.Connection = get_db()
    db.execute(
        """
        DELETE FROM Shopping_Cart WHERE ProductID = ?
        """,
        (product_id,)
    )
    db.commit()
    return redirect(url_for('shop.shopping_cart'))


@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout() -> Union[str, Response]:
    db: sqlite3.Connection = get_db()
    update_old_cart_items(db)
    if request.method == 'POST':
        error: str | None = None
        order_details = {'Name' : request.form['name'],
                        'Address' : request.form['address'],
                        'City' : request.form['city'],
                        'Region' : request.form['region'],
                        'PostalCode' : request.form['postal_code'],
                        'Country' : request.form['country']
        }
        for key, value in order_details.items():
            if not value:
                error = f'{key} is required.'

        if error is not None:
            flash(error)
        else:
            employee = db.execute(
                """
                SELECT EmployeeID FROM Employees WHERE (LastName, FirstName) = (?, ?)
                """,
                ('WEB', 'WEB')
            ).fetchone()
            db.execute(
                """
                INSERT INTO Orders (CustomerID, EmployeeID, ShipName, 
                ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (session.get('userID'), employee['EmployeeID'], order_details['Name'],
                 order_details['Address'], order_details['City'], order_details['Region'],
                 order_details['PostalCode'], order_details['Country'])
            )
            update_stock(db)
            shopper_id: str | None = session.get('session_id')
            db.execute(
                """
                DELETE FROM Shopping_Cart WHERE shopperID = ?
                """,
                (shopper_id,)
            )
            db.commit()
            return redirect(url_for('shop.done'))

    return render_template('shop/checkout.html')


@bp.route('/cart', methods=('GET', 'POST'))
def shopping_cart() -> str:
    db: sqlite3.Connection = get_db()
    cart = db.execute(
        """
        SELECT S.ProductID, ProductName, Quantity, TotalPrice, UnitPrice, 
        (UnitPrice * Quantity) AS ItemPrice 
        FROM Shopping_Cart AS S, Products AS P, 
            (SELECT SUM(UnitPrice * Quantity) as TotalPrice 
             FROM Shopping_Cart AS S, Products AS P 
             WHERE S.ProductID = P.ProductID) 
        WHERE S.ProductID = P.ProductID 
        GROUP BY ProductName
        """
    ).fetchall()
    empty: bool = True
    total: int = 0
    if len(cart) > 0:
        total = cart[0]['TotalPrice']
        empty = False

    return render_template('shop/cart.html', cart=cart, total=total, empty=empty)
