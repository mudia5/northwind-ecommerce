# Project 1: Online Commerce 

## The Databasers Team
**Team Lead:** Osamudiamen (Mudia) Eastwood - mudia5

**Development Engineer:** Matt Eichelman - meichelman

**Test Engineer:** Andrew Kallmeyer - AndrewKallmeyer1

**Documentation Specialist:** Julia Lin - julialin214

*Roles will rotate in future projects.* <br><br>






## Set Up

### 1. Clone this repository 

`git clone https://github.com/mudia5/northwind-ecommerce.git`

### 2. Download a local copy of the Northwind database

See instructions [here.](https://github.com/jpwhite3/northwind-SQLite3?tab=readme-ov-file)  

### 3. Move `northwind.db` into northwind-ecommerce/app

### 4. Create and activate a virtual environment
On macOS/Linux:
`python -m venv venv`
`source venv/bin/activate`

On Windows:
`python -m venv venv`
`venv\Scripts\activate`

### 5. Install dependencies 
`pip install -r requirements.txt`

### 6. Initialize the database 
`flask --app app init-db`

### 7. Run the server 
`flask --app app run --debug`<br><br>

## Testing
### Running the tests

**Run all tests:**

`python3 -m pytest`

**Run tests with coverage:**

`coverage run -m pytest`

**View coverage report:**

`coverage report`

`coverage html`

`open htmlcov/index.html`
 <br/><br/>
### Approach to testing 

We followed a **Test-Last (Traditional) approach**, where the code was implemented first and tests were written afterward to validate functionality, allowing us to iterate quickly during development. We focused on **unit testing**, where we validated individual functions in isolation. We structured our tests by writing a dedicated test file for each application module, systematically testing each function one by one. To maximize coverage, we wrote additional tests and incorporated parameterized testing to ensure each branch within a function was called. Since some functions involved database interactions and session management, many of these unit tests also served as **integration tests**, verifying that components such as database queries, authentication, and session handling worked together correctly. We used pytest and Flask’s test client to automate our testing process. By combining these approaches, we achieved a **comprehensive test coverage of 92%**, validating both individual functions and cross-component interactions to ensure the reliability of our application.

### Description of tests 

**`test_factory.py`**
contains tests for the application factory function, ensuring that the Flask app is correctly configured.  
- `test_config` verifies that the TESTING flag is enabled when passed as an argument and the app is configured accordingly.
- `test_hello` ensures that a simple test route (/hello) returns the expected response, providing a foundational check that the application starts with the correct configuration and can handle basic routes.
<br/><br/>

**`test_db.py`** tests the application's database connection and initialization to ensure proper database handling and setup.
- `test_get_close_db` tests that within an application context, `get_db` returns the same connection each time it’s called and that after the context, the connection is closed. 
- `test_init_db_command` tests that the application's database initialization command `init-db` calls the `init-db` function and outputs a message. It uses monkeypatching to replace the `init_db` function with a mock version `fake_init_db` that records when it's been called. 
<br/><br/>


**`test_auth.py`** tests the authentication system, including user registration, login, validation, and logout. It ensures that users can successfully register and log in while handling invalid inputs appropriately. Parameterized testing is used to check multiple invalid input cases efficiently, maximizing coverage.
- `test_register` verifies that users can access the registration page and successfully register with valid credentials. It ensures that a successful registration request redirects users to the login page (/auth/login).
-	`test_register_validate_input` uses parameterized testing to check multiple invalid registration attempts, including missing usernames, usernames that are too short or too long, and missing passwords. It ensures that appropriate error messages are returned for invalid inputs.
-	`test_login` tests that users can access the login page and successfully log in after registration. This test also interacts with the database to verify that a newly registered user is stored before attempting login.
-	`test_login_validate_input` uses parameterized testing to validate incorrect login attempts, such as using a non-existent username or an incorrect password. It checks that meaningful error messages are returned when authentication fails.
-	`test_logout` ensures that a logged-in user can successfully log out and that their session is properly cleared.
<br/><br/>


**`test_shop.py`** tests the e-commerce functionality of the application, covering product browsing/searching, the shopping cart, checkout, and DB stock updates. Parameterized testing is also used to check various invalid inputs for cart operations, maximizing test coverage.
- Homepage and Product Page
   - `test_shop_homepage` verifies that the homepage loads successfully and contains expected content.
   - `test_product_page` ensures that individual product pages can be accessed and correctly display the "Add to Cart" button if the product exists.
- Cart and Checkout
   - `test_cart_page` ensures that the cart page loads properly and displays an "empty cart" message when there are no items.
   - `test_add_to_cart` tests adding a product to the cart and checks for a successful redirect.
   - `test_clear_cart` verifies that users can successfully clear their shopping cart.
   - `test_remove_item` checks that users can remove items from their cart.
   - `test_checkout` tests the checkout process and verifies that users are redirected or see an order confirmation.
   - `test_guest_cannot_checkout` ensures that unauthenticated users cannot complete a checkout.
   - `test_update_stock` Ensures that product stock is updated in the DB correctly after a purchase.
- Invalid Cart Operations
   - `test_add_to_cart_invalid` uses parameterized testing to check invalid cart operations (e.g., missing product ID, missing quantity, product not found).
   - `test_item_invalid_quantity` ensures that invalid quantities (non-numeric values, empty inputs, excessive values) are handled properly.
- Product Search and Browse 
   - `test_search_page` ensures that the search page loads correctly and validates input requirements.
   - `test_search_results` tests that the search results page can be accessed.
   - `test_categories_page` verifies that the category listing page loads correctly.
   - `test_products_in_category` ensures that users can view products in a category.
- Session Management 
   - `test_update_old_cart_items` tests that items from an old shopping session transfer to a new session.
   - `test_update_old_cart_items_no_old_session` ensures that the system handles cases where no old session exists.
- Navigation Test
   - `test_continue_shopping_redirect` ensures that users are redirected correctly when choosing to continue shopping.
<br/><br/>
## Special Features 
### Shopping Cart Page
One of the most notable features we added is the **Shopping Cart page**, where users can view all products they have added to their cart. This page reflects the `Shopping_Cart` relation in the database and provides several key functionalities:

* **Visualizing Cart Items:** Users can see all the items in their cart, helping them keep track of their selections.
* **Item Removal Options:** Users can remove individual products or clear the entire cart in one action.
* **Price Display:** Each item displays its individual price, quantity added, and total item price. The total cart price is also displayed.
* **Quantity Adjustment:** While there isn’t a direct quantity update option, users can remove an item and re-add it with a different quantity, effectively updating their selection.
* **Checkout Process:**
    * Users can proceed to checkout only if the cart is non-empty. If the cart is empty, a notice is displayed.
    * Upon successful checkout, the cart is emptied.
 
### Additional features
**Improved Usability & Navigation**

To enhance usability, we implemented navigation buttons on each page:
* **Go Back** – Returns to the previous page
* **Go to Home** – Redirects to the homepage
* **Go to Shopping Cart** – Takes users directly to their cart

**Quantity & Stock Management**

To ensure stock accuracy and prevent errors, we implemented several quantity checks:
* **Stock Deduction on Checkout** – When a user checks out, the units in stock are  reduced in the database.
* **Preventing Over-Purchasing** – Users cannot add more quantity than what is currently in stock.
* **Preventing Invalid Additions** – Users cannot add 0 quantity to the cart, preventing out-of-stock items from being added.

