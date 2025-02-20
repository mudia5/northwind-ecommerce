import sqlite3
import os

DB_PATH = "app/northwind.db"
TEST_DB_PATH = "app/test_northwind.db"
SCHEMA_PATH = "app/schema.sql"

def initialize_db(db_path=DB_PATH): 

    if os.path.exists(db_path):
        os.remove(db_path)
    
    try: 
        with sqlite3.connect(db_path) as connect:
            cursor = connect.cursor()
            print(f"Connected to the {db_path}.")

        with open(SCHEMA_PATH, "r") as schemaf:
            schema_sql = schemaf.read()
            cursor.executescript(schema_sql)
            print("Database schema created successfully.")

        print(f"Database {db_path} initialization complete successfully.")

    except Exception as e: 
        print(f"Error initializing database: {e}")

def insert_test_data(db_path=TEST_DB_PATH):

    with sqlite3.connect(db_path) as conn: 
        cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO Authentication (userID, password, sessionID) VALUES ('TEST01', 'hashed_password_example', NULL);""")

    cursor.execute("""INSERT INTO Shopping_Cart (shopperID, productID, quantity, title) VALUES ('ABC123', 1, 2, 'Test Product');""")

    conn.commit()
    print("Test data inserted successfully.")


if __name__ == "__main__":
    initialize_db(TEST_DB_PATH)
    insert_test_data(TEST_DB_PATH)