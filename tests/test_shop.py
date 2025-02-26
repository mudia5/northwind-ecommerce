import pytest
from flask import session
from app.db import get_db
from app.shop import update_stock, update_old_cart_items


def test_shop_homepage(client) -> None:
    response = client.get('/')
    assert response.status_code == 200
    assert b"Online Shopping" in response.data


def test_product_page(client) -> None:
    response = client.get('/1/item')
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert b"Add to Cart" in response.data


def test_add_to_cart(client, auth) -> None:
    auth.login()
    response = client.post('/1/item', data={'product_id': 1, 'quantity': 2})
    assert response.status_code in [200, 302]

    if response.status_code == 302:
        assert "Location" in response.headers
        assert response.headers["Location"] in ["/cart", "/continue"]


def test_cart_page(client, auth) -> None:
    auth.login()
    response = client.get('/cart')
    assert response.status_code == 200
    assert b"Cart is empty" in response.data


def test_checkout(client, auth) -> None:
    auth.login()
    response = client.post('/checkout', data={'payment_method': 'card'})
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert "Location" in response.headers
    else:
        assert b"Order Confirmed" in response.data


@pytest.mark.parametrize(('product_id', 'quantity', 'message'), [
    ('', '2', 'Invalid product ID'),
    ('1', '', 'Quantity is required'),
    ('9999', '2', 'Product not found')
])
def test_add_to_cart_invalid(client, auth, product_id, quantity, message) -> None:
    auth.login()
    response = client.post('/1/item', data={'product_id': product_id, 'quantity': quantity})

    if response.status_code == 302:
        assert "Location" in response.headers
        assert response.headers["Location"] in ["/continue", "/1/item"]
    elif response.status_code == 200:
        assert message.encode() in response.data
    else:
        assert response.status_code == 400


def test_guest_cannot_checkout(client) -> None:
    response = client.post('/checkout', data={'payment_method': 'card'})
    assert response.status_code in [302, 403]
    if response.status_code == 302:
        assert "Location" in response.headers


def test_search_page(client) -> None:
    """Test search page rendering and validation."""
    response = client.get('/search')
    assert response.status_code == 200
    assert b"<title>Search - Online Shopping</title>" in response.data

    response = client.post('/search', data={'name': ''})
    assert response.status_code == 200
    assert b"Name is required" in response.data


def test_search_results(client) -> None:
    """Test search results route with a fake search."""
    response = client.get('/fakeproduct/search-results')
    assert response.status_code == 200


def test_categories_page(client) -> None:
    """Test category listing page."""
    response = client.get('/categories')
    assert response.status_code == 200
    assert b"<title>Categories - Online Shopping</title>" in response.data


def test_products_in_category(client) -> None:
    """Test products within a category."""
    response = client.get('/1/products')
    assert response.status_code in [200, 404]


def test_clear_cart(client, auth) -> None:
    """Test clearing the shopping cart."""
    auth.login()
    response = client.get('/clear_cart')
    assert response.status_code == 302


def test_update_stock(client, auth, app) -> None:
    """Test stock updates after checkout."""
    auth.login()

    with app.app_context():
        db = get_db()

        db.execute("DELETE FROM Products WHERE ProductID = 1")

        db.execute("""
            INSERT INTO Products (ProductID, ProductName, QuantityPerUnit, UnitPrice, UnitsInStock, CategoryID)
            VALUES (1, 'Test Product', '1 unit', 9.99, 10, 1)
        """)

        db.commit()

    with client.session_transaction() as sess:
        sess['session_id'] = 'test_session_123'

    with client.session_transaction() as sess:
        shopper_id = sess.get('session_id')

    assert shopper_id is not None

    with app.app_context():
        db = get_db()
        db.execute("""
            INSERT INTO Shopping_Cart (shopperID, productID, quantity)
            VALUES (?, ?, ?)
        """, (shopper_id, 1, 2))

        db.commit()

        update_stock(db)

        updated_stock = db.execute(
            """
            SELECT UnitsInStock FROM Products WHERE ProductID = ?
            """,
            (1,)).fetchone()
        assert updated_stock['UnitsInStock'] == 8


def test_update_old_cart_items(client, auth, app) -> None:
    """Test updating old cart items with new session."""
    auth.login()

    with app.test_request_context():
        session['old_session_id'] = 'old123'
        session['session_id'] = 'new123'

        with app.app_context():
            db = get_db()
            db.execute("""
                       INSERT INTO Shopping_Cart (shopperID, productID, quantity) VALUES ('old123', 1, 2)
                       """
                       )
            db.commit()

            update_old_cart_items(db)

            updated_cart = db.execute(
                """
                SELECT * FROM Shopping_Cart WHERE shopperID = 'new123'
                """
                ).fetchall()
            assert len(updated_cart) > 0


@pytest.mark.parametrize(('quantity', 'message'), [
    ('abc', 'Input quantity contains non-numeric characters.'),
    ('', 'Quantity is required.'),
    ('10000', 'Quantity exceeds what is in stock.')
])
def test_item_invalid_quantity(client, auth, quantity, message) -> None:
    auth.login()
    response = client.post('/1/item', data={'quantity': quantity})
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert "Location" in response.headers


def test_update_old_cart_items_no_old_session(client, app) -> None:
    with app.test_request_context():
        session.clear()
        with app.app_context():
            db = get_db()
            update_old_cart_items(db)


def test_remove_item(client, auth, app) -> None:
    auth.login()
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO Shopping_Cart (shopperID, productID, quantity) VALUES (?, ?, ?)",
                   ('test_session', 1, 2))
        db.commit()

    response = client.get('/1remove_item')
    assert response.status_code == 302

    with app.app_context():
        db = get_db()
        result = db.execute("SELECT * FROM Shopping_Cart WHERE ProductID = 1").fetchall()
        assert len(result) == 0


def test_continue_shopping_redirect(client) -> None:
    with client.session_transaction() as sess:
        sess.pop('user_id', None)

    response = client.get('/continue')
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['url'] == '/continue'
