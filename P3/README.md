# Project 1: Online Commerce 

## The Databasers Team
**Team Lead:** Osamudiamen (Mudia) Eastwood - mudia5

**Development Engineer:** Matt Eichelman - meichelman

**Test Engineer:** Andrew Kallmeyer - AndrewKallmeyer1

**Documentation Specialist:** Julia Lin - julialin214

<br><br>






## Set Up

### 1. Clone this repository 

`git clone https://github.com/mudia5/northwind-ecommerce.git`

### 2. Create and activate a virtual environment

On macOS/Linux:
`python -m venv .venv`
`. .venv/bin/activate`

On Windows:
`python -m venv venv`
`venv\Scripts\activate`

### 3. Install dependencies 

`pip install -r requirements.txt`

### 4. Create a local copy of the Boston Area Activities database

`cd app`

`sqlite3 boston_activities.db < schema.sql`

### 5. Populate `boston_actitivies.db` with data

`python3 generate_data.py`

The deprecation messages may be ignored as they do not affect the output.

`cd ..`

<!-- ### 6. Initialize the database

`flask --app app init-db` -->

### 6. Run the server

`flask --app app run --debug`

<br><br>

## Testing
### Running the tests

**Run all tests:**

`python -m pytest`

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
