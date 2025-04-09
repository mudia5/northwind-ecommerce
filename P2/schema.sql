
DROP TABLE IF EXISTS Groups;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Photos;
DROP TABLE IF EXISTS Phone_Number;
DROP TABLE IF EXISTS Group_Membership;
DROP TABLE IF EXISTS Attending;
DROP TABLE IF EXISTS Involved;
DROP TABLE IF EXISTS Themed;
DROP TABLE IF EXISTS Group_Membership;
DROP TABLE IF EXISTS Attending;
DROP TABLE IF EXISTS Involved;
DROP TABLE IF EXISTS Themed;



CREATE TABLE Groups (
    group_name VARCHAR(50) PRIMARY KEY,
    group_description TEXT NOT NULL,
    contact_email VARCHAR(100) NOT NULL,
    website_url TEXT,
    age_restriction INTEGER DEFAULT 0,
    sign_up_price INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE Categories (
    category_name VARCHAR(50) PRIMARY KEY,
    category_description TEXT NOT NULL
);

CREATE TABLE Locations (
    location_name VARCHAR(100) PRIMARY KEY,
    street_number INTEGER NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    zip INTEGER NOT NULL
);

CREATE TABLE Events (
    event_id INTEGER PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    time_of_day TIMESTAMP NOT NULL,
    max_attendees INTEGER NOT NULL,
    current_attendees INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (location_name) REFERENCES Locations
    -- Trigger statement below to update current_attendees
);

CREATE TABLE Review (
    review_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_name INTEGER,
    event_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES Users,
    FOREIGN KEY (group_name) REFERENCES Groups,
    FOREIGN KEY (event_id) REFERENCES Events
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone_id INTEGER UNIQUE,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    FOREIGN KEY (phone_id) REFERENCES Phone_Number(phone_id)
);

CREATE TABLE Photos (
    photo_id INTEGER PRIMARY KEY,
    photo IMAGE NOT NULL,
    photo_description TEXT NOT NULL,
    group_name INTEGER NOT NULL,
    FOREIGN KEY (group_name) REFERENCES Groups
);

CREATE TABLE Phone_Number (
    phone_id INTEGER,
    phone_number INTEGER,
    PRIMARY KEY (phone_id, phone_number)
);

CREATE TABLE Group_Membership (
    group_name INTEGER,
    user_id INTEGER,
    -- Trigger statement below to enforce age restriction
    user_role VARCHAR(50) NOT NULL,
    join_date DATE NOT NULL,
    is_registered BOOLEAN DEFAULT FALSE,
    register_time TIMESTAMP NOT NULL,
    PRIMARY KEY (group_name, user_id),
    FOREIGN KEY (group_name) REFERENCES Groups,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Attending (
    user_id INTEGER,
    event_id INTEGER,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE Involved (
    group_name VARCHAR(50),
    event_id INTEGER,
    PRIMARY KEY (group_name, event_id),
    FOREIGN KEY (group_name) REFERENCES Groups,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE Themed (
    group_name VARCHAR(50),
    category_name VARCHAR(50),
    PRIMARY KEY (group_name, category_name),
    FOREIGN KEY (group_name) REFERENCES Groups,
    FOREIGN KEY (category_name) REFERENCES Categories(category_name)
);


-- CREATE OR REPLACE FUNCTION check_age_restriction()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     IF (SELECT DATE_PART('year', AGE(NEW.date_of_birth)) < 
--         (SELECT age_restriction FROM Groups WHERE group_name = NEW.group_name)) THEN
--         RAISE EXCEPTION 'User does not meet the age restriction';
--     END IF;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER enforce_age_restriction
-- BEFORE INSERT ON Group_Membership
-- FOR EACH ROW EXECUTE FUNCTION check_age_restriction();


-- CREATE OR REPLACE FUNCTION update_attendees_count()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     UPDATE Events
--     SET current_attendees = (
--         SELECT COUNT(*) FROM Attending WHERE event_id = NEW.event_id
--     )
--     WHERE event_id = NEW.event_id;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER increment_attendees
-- AFTER INSERT OR DELETE ON Attending
-- FOR EACH ROW EXECUTE FUNCTION update_attendees_count();
