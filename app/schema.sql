
DROP TABLE IF EXISTS Authentication;
DROP TABLE IF EXISTS Shopping_Cart;

CREATE TABLE Authentication (
  userID TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  sessionID TEXT, 
  FOREIGN KEY (userID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Shopping_Cart (
  shopperID TEXT NOT NULL,
  productID INTEGER NOT NULL,
  QUANTITY INTEGER NOT NULL CHECK (QUANTITY > 0),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Employees (LastName, FirstName)
VALUES ('WEB', 'WEB');
