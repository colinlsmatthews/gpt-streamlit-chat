import sqlite3


def create_database():
    # Connect to SQLite database (it will create the file if not exists)
    conn = sqlite3.connect('profiles.db')

    # Create a table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS profiles
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT,
    description TEXT);
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Initialize the database
create_database()
