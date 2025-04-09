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


def generate_users_data(c: sqlite3.Cursor) -> None:
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
                        INSERT INTO [Users] (first_name, middle_initial, last_name, email, phone_id, date_of_birth, gender) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        '''
        last_name: str = last_names[randint(0, len(last_names) - 1)]
        email: str = f'{last_name}.{name}@gmail.com'
        phone_id: str = f'{randint(1000, 9999)}'
        gender: str = 'Male' if i <= 13 else 'Female'
        date_of_birth: date = random_date(
                datetime.strptime('1980-01-01', '%Y-%m-%d'),
                datetime.strptime('2000-01-01', '%Y-%m-%d'),
            )
        params: tuple[str, str, str, str, str, date, str] = (
            name,
            middle_initials[randint(0, 25)],
            last_name,
            email,
            phone_id,
            date_of_birth,
            gender
        )
        c.execute(command, params)
    print('Users data generated successfully!')


def generate_categories_data(c: sqlite3.Cursor) -> None:
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
                        INSERT INTO [Categories] (category_name, description) 
                        VALUES (?, ?)
                        '''
        params: tuple[str, str] = (
            name,
            descriptions[i]
        )
        c.execute(command, params)
    print('Categories data generated successfully!')


def main() -> None:
    """The main function"""
    db: sqlite3.Connection = sqlite3.connect('./boston_activities.db')
    c: sqlite3.Cursor = db.cursor()
    print('\nGenerating data...')
    generate_users_data(c)
    generate_categories_data(c)
    print('\n')

    db.commit()
    db.close()


if __name__ == '__main__':
    main()
