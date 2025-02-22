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
<br><br>

## Special Features 
### Shopping Cart Page
One of the most notable features we added is the **Shopping Cart page**, where users can view all products they have added to their cart. This page reflects the `Shopping_Cart` table in the database and provides several key functionalities:

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

