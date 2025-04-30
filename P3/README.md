# Project 3: A Real-World Database Application

This real-world database application offers **residents of the Boston area** a centralized platform to discover and engage with **local activity groups**. Users can browse groups by name or category, join communities, register for events, and even create and manage their own groups. The goal is to make it easier for individuals to connect with like-minded people and get involved in local activities through organized and reliable information.

<br>

## The Databasers Team
**Team Lead:** Osamudiamen (Mudia) Eastwood - mudia5

**Development Engineer:** Matt Eichelman - meichelman

**Test Engineer:** Andrew Kallmeyer - AndrewKallmeyer1

**Documentation Specialist:** Julia Lin - julialin214

<br><br>






## Deploying the Application 

### 1. Clone this repository 

`git clone https://github.com/mudia5/northwind-ecommerce.git`

`cd northwind-ecommerce/`

<br>

### 2. Create and activate a virtual environment

On macOS/Linux:


`python3 -m venv .venv`

`. .venv/bin/activate`

On Windows:


`python -m venv .venv`

`attrib +h .venv`

`.venv\Scripts\Activate.ps1`

<br>

### 3. Install dependencies 

`cd P3/`

`pip3 install -r requirements.txt`

<br>

### 4. Create a local copy of the Boston Area Activities database

`cd app/`

`sqlite3 boston_activities.db < schema.sql`

<br>

### 5. Populate `boston_activities.db` with data

`python3 generate_data.py` // _The deprecation messages may be ignored as they do not affect the output._

`cd ..`

<!-- ### 6. Initialize the database

`flask --app app init-db` -->

<br>


### 6. Run the server

`flask --app app run --debug`

Look for the `Running on http://127.0.0.1:5000` message and visit the printed url in your browser 

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

## Special Features
