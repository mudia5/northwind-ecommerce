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

<br>

### 6. Initialize the database

`flask --app app init-db`

<br>


### 7. Run the server

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
- `test_write_review_invalid_rating(client, app)` ensures that submitting a review with an out-of-range rating (e.g., 6) does not insert the review and instead shows the appropriate error message. 
- `test_write_review_empty_comment(client, app)` verifies that submitting a review with an empty comment defaults the comment to "N/A" and successfully redirects to the review page without error.
- `test_delete_nonexistent_review(client, app)` tests deletion of a non-existent review and expects a TypeError, verifying error handling for missing reviews.
- `test_create_event_invalid_time_format(client, app)` attempts to create an event with an invalid time string and confirms the error message is rendered.
- `test_create_event_past_time(client, app)` ensures that creating an event with a time in the past is blocked and an appropriate error message is shown.
- `test_remove_expired_events_runs(client, app)` confirms that past events are removed.
<br/><br/>

**`test_generate_data.py`** verifies the data generation script for populating the database with synthetic data. 
- `test_generate_groups_raises_operational_error()` confirms that generate_groups raises an OperationalError if the cursor fails.
- `test_main_runs_without_crash(tmp_path)` verifies that the full `main()` function in `generate_data.py` runs without errors and correctly initializes the database with required tables.
- `test_generate_groups(db_cursor)` tests that `generate_groups()` correctly populates the **Groups** table with exactly 2 records.
- `test_generate_categories(db_cursor)` ensures `generate_categories()` populates the **Categories** table with 7 entries.
- `test_generate_locations(db_cursor)` checks that `generate_locations()` inserts 7 entries into the **Locations** table.
- `test_generate_zipcity(db_cursor)` verifies `generate_zipcity()` fills the **Zip_City** table with 7 entries.
- `test_generate_events(db_cursor)` first generates required locations, then confirms `generate_events()` adds 2 entries to the **Events** table.
- `test_generate_review(db_cursor)` after generating users, locations, and events, checks that `generate_review()` creates 2 review entries.
- `test_generate_users(db_cursor)` confirms that `generate_users()` inserts 20 user records.
- `test_generate_userphone(db_cursor)` after generating users, ensures `generate_userphone()` adds 21 phone records (some users may have multiple).
- `test_generate_belongs(db_cursor)` verifies that `generate_belongs()` inserts 2 records linking groups to categories.
- `test_generate_membership(db_cursor)` ensures that `generate_membership()` links users to groups with 21 records in the **Membership** table.
- `test_generate_attending(db_cursor)` checks that `generate_attending()` inserts 21 event attendance records.
- `test_generate_hosts(db_cursor)`confirms that `generate_hosts()` creates 2 valid host relationships between groups and events.
- `test_all_generators_with_mock_cursor()` runs all generator functions using a mocked cursor to verify that each function executes without raising unexpected errors.
<br/><br/>

**`test_groups.py`** validates  group-related functionality, including group creation, joining/leaving a group, and handling duplicate signups. 
- `test_create_group(client, app)` verifies that a logged-in user can successfully create a group.
- `test_signup_and_leave_group(client, app)` tests that a user can sign up for a group and then leave it.
- `test_signup_twice(client, app)` checks that a second attempt to join the same group returns an error message. 
<br/><br/>

**`test_init.py`** verifies the setup and configuration of the Flask application.
- `test_create_app_default_config()` checks that the app initializes correctly with default settings.
- `test_create_app_test_config()` verifies that the app correctly loads a test configuration (TESTING=True) while preserving default config values. 
- `test_instance_folder_creation(monkeypatch, tmp_path)` ensures that the application can be initialized with a custom instance path, and that folder creation logic does not raise errors. 
- `test_init_db_creates_schema(tmp_path, monkeypatch)` mocks a schema file and a database path, then confirms that init_db() correctly creates the expected schema table.
- `test_init_db_command(runner)` runs the init-db command and asserts that it completes successfully with the expected confirmation message.
<br/><br/>

**`test_locations.py`** verifies the functionality of adding new locations by authenticated users. 
- `test_get_add_location_form(client, app)` verifies that a logged-in user can access the "Add Location" form with the expected fields. 
- `test_post_add_location(client, app)` tests that submitting valid location data via POST results in a successful redirect or page load. 
<br/><br/>


## Special Features

### Events
In addition to supporting activity groups across the Boston area, our application offers functionality for **managing local events** hosted by those groups. Users can browse upcoming events, register to attend, host their own, and even leave reviews. Event sign-ups are tracked in real time, and integrity constraints ensure that attendance never exceeds the maximum capacity specified by the event host. In doing so, our platform provides **a centralized hub** for any and all information Boston residents might need to engage with local communities and events. 

### Authentication
Our application includes a user authentication system that allows individuals to register accounts and **access personalized features**. Logged-in users can manage their group memberships and event registrations, create events, submit reviews, and access pages restricted to authenticated users. If an unauthenticated user attempts to access the create event or create group forms, they are redirected to the login page, ensuring secure and appropriate **access control**.

### Error Handling
To maintain the consistency and reliability of the data, we implemented extensive integrity constraints in the Project 2 database design, particularly NOT NULL and CHECK constraints. In the web application, we built on this foundation by incorporating front-end and back-end error handling to **prevent system crashes** and instead provide **informative feedback** to users. For example, the event creation form displays clear error messages when an invalid date is submitted (e.g., a past date or incorrect format), and the review submission form warns users if a rating falls outside the valid 1–5 range. Furthermore, forms cannot be submitted if the required fields are blank. 

### Flexibility
We intentionally designed our forms to be **flexible** and **user-friendly**. Many input fields are optional, allowing for greater customization and ease of use. Event hosts may choose whether to set a maximum attendee limit, group creators can optionally define age restrictions, and users can submit ratings with or without accompanying comments. 

