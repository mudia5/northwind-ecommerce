-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;

CREATE TABLE Authentication (
  userID TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  sessionID TEXT
);

CREATE TABLE Shopping_Cart (
  shopperID TEXT NOT NULL,
  productID INTEGER NOT NULL,
  QUANTITY INTEGER NOT NULL CHECK (quantity > 0),
  title TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Employees (
    (LastName, FirstName)
    VALUES ('WEB', 'WEB')
);
