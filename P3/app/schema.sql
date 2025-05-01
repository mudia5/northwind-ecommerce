
DROP TABLE IF EXISTS Groups;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Zip_City;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Photos;
DROP TABLE IF EXISTS User_Phone;
DROP TABLE IF EXISTS Belongs;
DROP TABLE IF EXISTS Membership;
DROP TABLE IF EXISTS Attending;
DROP TABLE IF EXISTS Hosts;



CREATE TABLE Groups (
    group_name VARCHAR(50) PRIMARY KEY,
    group_description TEXT NOT NULL,
    contact_email VARCHAR(100) NOT NULL,
    website_url TEXT,
    min_age INTEGER CHECK (min_age > 0),
    max_age INTEGER CHECK (max_age > 0),
    sign_up_price INTEGER CHECK (sign_up_price >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    register_date DATE
);

CREATE TABLE Categories (
    category_name VARCHAR(50) PRIMARY KEY,
    category_description TEXT NOT NULL
);

CREATE TABLE Locations (
    location_name VARCHAR(100) PRIMARY KEY,
    street_number INTEGER NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    zip INTEGER NOT NULL
);

CREATE TABLE Zip_City (
    zip INTEGER PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    FOREIGN KEY (zip) REFERENCES Locations(zip)
);

CREATE TABLE Events (
    event_id INTEGER PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    location_name VARCHAR(100) NOT NULL,
    time_of_day TIMESTAMP NOT NULL,
    max_attendees INTEGER CHECK (max_attendees > 0),
    current_attendees_count INTEGER NOT NULL CHECK (current_attendees_count >= 0),
    FOREIGN KEY (location_name) REFERENCES Locations(location_name)
);

CREATE TABLE Review (
    review_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    password TEXT NOT NULL,
    sessionID TEXT
);

CREATE TABLE Photos (
    photo_id INTEGER PRIMARY KEY,
    photo IMAGE NOT NULL,
    photo_description TEXT NOT NULL,
    group_name varchar(50) NOT NULL,
    FOREIGN KEY (group_name) REFERENCES Groups(group_name)
);

CREATE TABLE User_Phone (
    user_id INTEGER,
    phone_number INTEGER,
    PRIMARY KEY (user_id, phone_number)
);

CREATE TABLE Belongs (
    group_name VARCHAR(50),
    category_name VARCHAR(50),
    PRIMARY KEY (group_name, category_name),
    FOREIGN KEY (group_name) REFERENCES Groups(group_name),
    FOREIGN KEY (category_name) REFERENCES Categories(category_name)
);

CREATE TABLE Membership (
    group_name VARCHAR(50),
    user_id INTEGER,
    user_role VARCHAR(50) NOT NULL CHECK (user_role IN ('admin', 'member', 'waitlist')),
    join_time TIMESTAMP NOT NULL,
    register_time TIMESTAMP NOT NULL,
    PRIMARY KEY (group_name, user_id),
    FOREIGN KEY (group_name) REFERENCES Groups(group_name),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Attending (
    user_id INTEGER,
    event_id INTEGER,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);

CREATE TABLE Hosts (
    group_name VARCHAR(50),
    event_id INTEGER,
    PRIMARY KEY (group_name, event_id),
    FOREIGN KEY (group_name) REFERENCES Groups(group_name),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);


CREATE TRIGGER update_attendee_count_after_insert
AFTER INSERT ON Attending
FOR EACH ROW
BEGIN
    UPDATE Events
    SET current_attendees_count = (
        SELECT COUNT(*)
        FROM Attending
        WHERE event_id = NEW.event_id
    )
    WHERE event_id = NEW.event_id;
END;


CREATE TRIGGER update_attendee_count_after_delete
AFTER DELETE ON Attending
FOR EACH ROW
BEGIN
    UPDATE Events
    SET current_attendees_count = (
        SELECT COUNT(*)
        FROM Attending
        WHERE event_id = OLD.event_id
    )
    WHERE event_id = OLD.event_id;
END;


CREATE TRIGGER invalid_event_creation
BEFORE INSERT ON Events
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN NEW.current_attendees_count != 0
            THEN RAISE(ABORT, 'New events require an initial 0 attendees.')
        END;
END;


CREATE TRIGGER membership_age_invalid
BEFORE INSERT ON Membership
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN (
                (SELECT CAST((julianday('now') - julianday(date_of_birth)) / 365.25 AS INTEGER)
                 FROM Users
                 WHERE user_id = NEW.user_id
                ) < (SELECT min_age FROM Groups WHERE group_name = NEW.group_name)
                OR
                (SELECT CAST((julianday('now') - julianday(date_of_birth)) / 365.25 AS INTEGER)
                 FROM Users
                 WHERE user_id = NEW.user_id
                ) > (SELECT max_age FROM Groups WHERE group_name = NEW.group_name)
            )
            THEN RAISE(ABORT, 'User does not meet the age requirement for this group.')
        END;
END;


CREATE TRIGGER event_full
BEFORE INSERT ON Attending
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN (
                SELECT current_attendees_count
                FROM Events
                WHERE event_id = NEW.event_id
            ) >= (
                SELECT max_attendees
                FROM Events
                WHERE event_id = NEW.event_id
            )
            THEN RAISE(ABORT, 'This event is at maximum capacity.')
        END;
END;
