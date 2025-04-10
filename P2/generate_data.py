"""
Script to generate dummy date for the database.
"""


from datetime import timedelta, datetime, date
from random import randint
import sqlite3


def random_date(start: datetime, end: datetime) -> date:
    """Generate a random date"""
    delta = end - start
    random_seconds = randint(0, int(delta.total_seconds()))
    random_datetime = start + timedelta(seconds=random_seconds)
    return random_datetime.date()


def generate_groups(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the groups table"""
    names: list[str] = ['The A-Team', 'Victory Is Ours']
    descriptions: list[str] = ['The best soccer players in all of Boston',
                               'An elite group of tennis players']
    emails: list[str] = ['Ateam@gmail.com', 'Victors@gmail.com']
    min_ages: list[int] = [18, 25]
    max_ages: list[int] = [40, 55]
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
    # cities: list[str] = ['Newton', 'Cambridge', 'Brookline', 'Somerville', 'Watertown',
    #                      'Belmont', 'Waltham']
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
            # cities[i],
            zips[i]
        )
        c.execute(command, params)
    try:
        print('Locations data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into locations table')

def generate_events(c: sqlite3.Cursor) -> None:
    """Generate dummy data for the events table"""
    location_names: list[str] = ['Newton Soccer Park', 'Elmwood Tennis Courts']
    times: list[datetime] = [datetime(2025, 4, 12, 12, 0, 0),
                             datetime(2025, 4, 13, 16, 0, 0)]
    attendees: list[int] = [36, 8]
    curr_att_count: int = 0
    for i, name in enumerate(location_names):
        command: str = '''
                        INSERT INTO [Events] (location_name, time_of_day, max_attendees, current_attendees_count) 
                        VALUES (?, ?, ?, ?)
                        '''
        params: tuple[str, datetime, int, int] = (
            name,
            times[i],
            attendees[i],
            curr_att_count
        )
        c.execute(command, params)
    try:
        print('Events data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into events table')


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
    for i, name in enumerate(first_names):
        command: str = '''
                        INSERT INTO [Users] (first_name, middle_initial, last_name, email, date_of_birth, gender) 
                        VALUES (?, ?, ?, ?, ?, ?)
                        '''
        last_name: str = last_names[randint(0, len(last_names) - 1)]
        email: str = f'{last_name}.{name}@gmail.com'
        gender: str = 'Male' if i <= 13 else 'Female'
        date_of_birth: date = random_date(
                datetime.strptime('1980-01-01', '%Y-%m-%d'),
                datetime.strptime('2000-01-01', '%Y-%m-%d'),
            )
        params: tuple[str, str, str, str, date, str] = (
            name,
            middle_initials[randint(0, 25)],
            last_name,
            email,
            date_of_birth,
            gender
        )
        c.execute(command, params)
    try:
        print('Users data generated successfully!')
    except sqlite3.OperationalError:
        print('Error inserting data into users table')


def main() -> None:
    """The main function"""
    db: sqlite3.Connection = sqlite3.connect('./boston_activities.db')
    c: sqlite3.Cursor = db.cursor()

    print('\nGenerating data...')
    generate_groups(c)
    generate_categories(c)
    generate_locations(c)
    generate_events(c)
    generate_users(c)
    print()

    db.commit()
    # Commit first, then continue with the rest of the code
    # Need to copy over the phone_ids from the users table after its committed
    db.close()


if __name__ == '__main__':
    main()
