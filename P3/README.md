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

1. Run all tests: `coverage run -m pytest`

2. View coverage report: `coverage report`

 
### Approach to testing 

Similar to Project 1, we followed a **Test-Last (Traditional) approach**, where the code was implemented first and tests were written afterward to validate functionality, allowing us to iterate quickly during development. We focused on **unit testing**, where we validated individual functions in isolation. We structured our tests by writing a dedicated test file for each application module, systematically testing each function one by one. To maximize coverage, we wrote additional tests to ensure each branch within a function was called. We used pytest and Flask’s test client to automate our testing process. We achieved a **comprehensive test coverage of 95%**, ensuring the reliability of our application.

### Description of tests 

**`test_auth.py`** contains tests for the authentication flow of the application, including user registration, login with valid/invalid credentials, and logout functionality. 
- `test_register_logout(client)`tests whether a user can successfully register and receive a redirect response, indicating the registration completed correctly.
- `test_login_valid_user(client)` ensures a user can log in using correct credentials after registration and verifies a successful login via redirect to the home page.
- `test_login_invalid_user(client)` tests login with invalid credentials and confirms that the response returns HTTP 400 and appropriate error messages for incorrect login information.
- `test_logout_clears_session(client)` verifies that logging out redirects the user to the home page. 
<br/><br/>


**`test_browse.py`** verifies the public and user-specific browsing features of the application, including viewing groups, categories, events, and user profile pages. 
- `test_index_page(client)`checks that the home page loads successfully.
- `test_groups_all_category(client, app)` verifies that all groups across categories are displayed properly after user login.
- `test_groups_specific_category(client, app)` ensures that a specific group category page (e.g., Music) is accessible and returns a successful response.
- `test_categories_page(client, app)` tests that the categories  page loads and displays the appropriate content.
- `test_locations_page(client, app)` checks that the locations browsing page is accessible and includes relevant location data such as ZIP codes.
- `test_mypage_authenticated(client, app)` verifies that a logged-in user can access their personal page with account-related content.
- `test_update_mypage_get(client, app)` ensures that the user profile update form is accessible via GET request for an authenticated user.
- `test_update_mypage_post(client, app)` tests submitting updated user info via POST to the profile update page and confirms successful redirect or load.
- `test_browse_events_no_filters(client, app)` confirms that all events are shown correctly.
<br/><br/>

**`test_categories.py`** verifies the functionality for creating categories by authenticated users. 
- `test_get_create_category_form(client, app)` ensures that a logged-in user can access the category creation form and that the form loads correctly with expected fields. 
- `test_post_create_category(client, app)` simulates a logged-in user submitting a new category with a name and description, confirming successful form handling and redirect.
<br/><br/>

**`test_events.py`** tests all event-related features including event creation, user registration for events, review writing/deleting, and system handling of edge cases like invalid inputs or expired events. 
- `test_event_creation(client, app)` verifies that a logged-in user can create a valid event.
- `test_see_review(client)' checks that the reviews page for event ID 1 loads correctly and contains expected content.
- `test_signup_and_drop_event(client, app)` tests whether a logged-in user can successfully sign up for and drop an event. 
- `test_delete_review(client, app)` ensures that the delete review route returns a valid status code (302 for success or 404 if not found).

**FIX THESE TWO**

- `test_write_review_invalid_rating(client, app)` attempts to post a review with an invalid rating (6) and expects an sqlite3.IntegrityError due to rating constraints. 
- `test_write_review_empty_comment(client, app)`
Tries to submit a review with an empty comment and expects an UnboundLocalError, revealing potential input handling issues.


- `test_delete_nonexistent_review(client, app)` tests deletion of a non-existent review and expects a TypeError, verifying error handling for missing reviews.
- `test_create_event_invalid_time_format(client, app)` attempts to create an event with an invalid time string and confirms the error message is rendered.
- `test_create_event_past_time(client, app)` ensures that creating an event with a time in the past is blocked and an appropriate error message is shown.
- `test_remove_expired_events_runs(client, app)` confirms that past events are removed. 



<br/><br/>
**`test_generate_data.py`**
<br/><br/>
**`test_groups.py`**
<br/><br/>
**`test_init.py`**
<br/><br/>
**`test_locations.py`**
<br/><br/>


## Special Features
