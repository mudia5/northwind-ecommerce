"""
Script to generate dummy date for the database.
"""


from datetime import timedelta, datetime, date
from random import randint, choice
import string
import sqlite3
from werkzeug.security import generate_password_hash


def random_date(start: datetime, end: datetime) -> date:
    """Generate a random date"""
    delta = end - start
    random_seconds = randint(0, int(delta.total_seconds()))
    random_date_date = start + timedelta(seconds=random_seconds)
    return random_date_date.date()


def random_datetime(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime"""
    delta = end - start
    random_seconds = randint(0, int(delta.total_seconds()))
    random_date_time = start + timedelta(seconds=random_seconds)
    return random_date_time


def generate_groups(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the groups table"""
    names: list[str] = ['The A-Team', 'Victory Is Ours']
    descriptions: list[str] = ['The best soccer players in all of Boston',
                               'An elite group of tennis players']
    emails: list[str] = ['Ateam@gmail.com', 'Victors@gmail.com']
    min_ages: list[int] = [18, 18]
    max_ages: list[int] = [65, 65]
    for i, name in enumerate(names):
        command: str = '''
                        INSERT INTO [Groups] (group_name, group_description, contact_email,
                        min_age, max_age) 
                        VALUES (?, ?, ?, ?, ?)
                        '''
        params: tuple[str, str, str, int, int] = (
            name,
            descriptions[i],
            emails[i],
            min_ages[i],
            max_ages[i]
        )
        c.execute(command, params)
    try:
        print('Groups data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into Groups table')


def generate_categories(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the categories table"""
    names: list[str] = ["Men's Soccer", "Women's Tennis", 'Co-Rec Softball',
                        'Cooking', 'Yoga', 'Art', 'Dance']
    descriptions: list[str] = ['Pick-up style soccer games for men',
                               'Casual tennis matches for women, singles or doubles',
                               'Softball games open to all genders, teams are mixed',
                               'Learn and try out new recipes with others',
                               'Relaxing group sessions focused on stretching and breathing',
                               'Chill creative time with painting, drawing, and more',
                               'Casual dance classes where you can move and have fun',]
    for i, name in enumerate(names):
        command: str = '''
                        INSERT INTO [Categories] (category_name, category_description) 
                        VALUES (?, ?)
                        '''
        params: tuple[str, str] = (
            name,
            descriptions[i]
        )
        c.execute(command, params)
    try:
        print('Categories data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into categories table')


def generate_locations(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the locations table"""
    names: list[str] = ['Newton Soccer Park', 'Elmwood Tennis Courts', 'Willow Softball Field',
                        'The Culinary Workshop', 'Harmony Yoga Studio',
                        'Maple Art Center', 'The Newton Dance Hall']
    numbers: list[int] = [randint(1000, 9999) for _ in range(7)]
    streets: list[str] = ['Main Street', 'Elm Street', 'Oak Street', 'Pine Street',
                          'Maple Avenue', 'Willow Road', 'Cedar Lane']
    zips: list[str] = ['02458', '02138', '02445', '02143', '02472', '02478', '02452']
    for i, name in enumerate(names):
        command: str = '''
                        INSERT INTO [Locations] (location_name, street_number, street_name, zip) 
                        VALUES (?, ?, ?, ?)
                        '''
        params: tuple[str, int, str, str] = (
            name,
            numbers[i],
            streets[i],
            zips[i]
        )
        c.execute(command, params)
    try:
        print('Locations data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into locations table')


def generate_zipcity(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the zip_city table"""
    zips: list[str] = ['02458', '02138', '02445', '02143', '02472', '02478', '02452']
    cities: list[str] = ['Newton', 'Cambridge', 'Brookline', 'Somerville', 'Watertown',
                         'Belmont', 'Waltham']
    for i, city in enumerate(cities):
        command: str = '''
                        INSERT INTO [Zip_City] (zip, city) 
                        VALUES (?, ?)
                        '''
        params: tuple[str, ...] = (
            zips[i],
            city
        )
        c.execute(command, params)
    try:
        print('Zip city data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into zip_city table')


def generate_events(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the events table"""
    location_names: list[str] = ['Newton Soccer Park', 'Elmwood Tennis Courts']
    event_names: list[str] = ['Soccer Game', 'Tennis Match']
    times: list[datetime] = [datetime(2025, 6, 12, 12, 0, 0),
                             datetime(2025, 6, 13, 16, 0, 0)]
    attendees: list[int] = [36, 8]
    curr_att_count: int = 0
    for i, location_name in enumerate(location_names):
        command: str = '''
                        INSERT INTO [Events] (location_name, event_name, time_of_day, max_attendees, current_attendees_count) 
                        VALUES (?, ?, ?, ?, ?)
                        '''
        params: tuple[str, str, datetime, int, int] = (
            location_name,
            event_names[i],
            times[i],
            attendees[i],
            curr_att_count
        )
        c.execute(command, params)
    try:
        print('Events data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into events table')


def generate_review(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the reviews table"""
    ratings: list[int] = [5, 4]
    user_ids: list[int] = [1, 15]
    event_ids: list[int] = [1, 2]
    comments: list[str] = ['Great event! I had a lot of fun and would recommend to a friend.',
                           'Met some great people and I will certainly come again!']
    for i, rating in enumerate(ratings):
        command: str = '''
                        INSERT INTO [Review] (user_id, event_id, rating, comment) 
                        VALUES (?, ?, ?, ?)
                        '''
        params: tuple[int, int, int, str] = (
            user_ids[i],
            event_ids[i],
            rating,
            comments[i]
        )
        c.execute(command, params)
    try:
        print('Review data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into review table')


def generate_users(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the users table"""
    first_names: list[str] = ['Matthew', 'John', 'Bob', 'Charlie', 'David',
                              'Frank', 'Ivan', 'Karl', 'Leo', 'Sam',
                              'Nick', 'Will', 'Hunter', 'Garrett', 'Jane',
                              'Alice', 'Eve', 'Grace', 'Heidi', 'Judy']
    middle_initials: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    last_names: list[str] = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown',
                        'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                        'Anderson', 'Thomas', 'Jackson', 'White', 'Harris',
                        'Peterson', 'Tukuru', 'Sweeney', 'Linton', 'McCloskey']
    characters: str = string.ascii_letters + string.digits + string.punctuation
    for i, name in enumerate(first_names):
        command: str = '''
                        INSERT INTO [Users] (first_name, middle_initial, last_name, email, date_of_birth, gender, password) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        '''
        last_name: str = last_names[randint(0, len(last_names) - 1)]
        email: str = f'{last_name}.{name}@gmail.com'
        gender: str = 'Male' if i <= 13 else 'Female'
        date_of_birth: date = random_date(
                datetime.strptime('1980-01-01', '%Y-%m-%d'),
                datetime.strptime('2000-01-01', '%Y-%m-%d'),
            )
        password: str = generate_password_hash(''.join(choice(characters) for _ in range(8)))
        params: tuple[str, str, str, str, date, str, str] = (
            name,
            middle_initials[randint(0, 25)],
            last_name,
            email,
            date_of_birth,
            gender,
            password
        )
        c.execute(command, params)
    try:
        print('Users data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into users table')


def generate_userphone(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the user_phone table"""
    user_ids: list[int] = [i for i in range(1, 22)]
    phone_numbers: list[int] = [int(f'{randint(100, 999)}{randint(100, 999)}{randint(1000, 9999)}')
                                for _ in range(21)]
    for i, user_id in enumerate(user_ids):
        command: str = '''
                        INSERT INTO [User_Phone] (user_id, phone_number) 
                        VALUES (?, ?)
                        '''
        params: tuple[int, ...] = (
            user_id,
            phone_numbers[i]
        )
        c.execute(command, params)
    try:
        print('User phone data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into user phone table')


def generate_belongs(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the belongs table"""
    group_names: list[str] = ['The A-Team', 'Victory Is Ours']
    category_names: list[str] = ["Men's Soccer", "Women's Tennis"]
    for i, group_name in enumerate(group_names):
        command: str = '''
                        INSERT INTO [Belongs] (group_name, category_name) 
                        VALUES (?, ?)
                        '''
        params: tuple[str, str] = (
            group_name,
            category_names[i]
        )
        c.execute(command, params)
    try:
        print('Belongs data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into belongs table')


def generate_membership(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the membership table"""
    group_names: list[str] = ['The A-Team', 'Victory Is Ours']
    user_ids: list[int] = [i for i in range(21)]
    join_times: list[datetime] = [random_datetime(
                datetime.strptime('2024-05-21', '%Y-%m-%d'),
                datetime.strptime('2024-05-26', '%Y-%m-%d'),
            ) for _ in range(21)]
    for i, user_id in enumerate(user_ids):
        command: str = '''
                        INSERT INTO [Membership] (group_name, user_id, user_role, join_time, register_time) 
                        VALUES (?, ?, ?, ?, ?)
                        '''
        user_role: str = 'member'
        if i in (0, 15):
            user_role = 'admin'
        group_name: str = group_names[0]
        if i > 14:
            group_name = group_names[1]
        join_times[0] = datetime(2024, 1, 10, 12, 0, 0)
        join_times[15] = datetime(2024, 5, 15, 12, 0, 0)
        params: tuple[str, int, str, datetime, datetime] = (
            group_name,
            user_id + 1,
            user_role,
            join_times[i],
            join_times[i]
        )
        c.execute(command, params)
    try:
        print('Membership data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into membership table')


def generate_attending(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the attending table"""
    event_id: int = 1
    user_ids: list[int] = [i for i in range(1, 22)]
    for user_id in user_ids:
        if user_id > 14:
            event_id = 2
        command: str = '''
                        INSERT INTO [Attending] (event_id, user_id) 
                        VALUES (?, ?)
                        '''
        params: tuple[int, int] = (
            event_id,
            user_id
        )
        c.execute(command, params)
    try:
        print('Attending data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into attending table')


def generate_hosts(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the hosts table"""
    event_ids: list[int] = [1, 2]
    names: list[str] = ['The A-Team', 'Victory Is Ours']
    for i, name in enumerate(names):
        command: str = '''
                        INSERT INTO [Hosts] (group_name, event_id) 
                        VALUES (?, ?)
                        '''
        params: tuple[str, int] = (
            name,
            event_ids[i]
        )
        c.execute(command, params)
    try:
        print('Hosts data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into hosts table')


def main() -> None:
    """The main function"""
    db: sqlite3.Connection = sqlite3.connect('./boston_activities.db')
    c: sqlite3.Cursor = db.cursor()

    print('\nGenerating data...')
    generate_groups(c)
    generate_categories(c)
    generate_locations(c)
    generate_zipcity(c)
    generate_events(c)
    generate_review(c)
    generate_users(c)
    generate_userphone(c)
    generate_belongs(c)
    generate_membership(c)
    generate_attending(c)
    generate_hosts(c)
    print('Success!\n')

    db.commit()
    db.close()


if __name__ == '__main__':
    main()
