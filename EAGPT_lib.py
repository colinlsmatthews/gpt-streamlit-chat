import os
import openai
import tiktoken
import glob
import sqlite3
import streamlit as st

# if "api_key" in st.session_state:
#     openai.api_key = st.session_state["api_key"]

# *************************************************************
# Setup functions


# *************************************************************
# Profile functions


PROFILE_DIR = "profiles\\"


def get_profile_files(extension=".txt"):
    return glob.glob(os.path.join(PROFILE_DIR, f"*{extension}"))


def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return file.read()


def get_filtered_file_list():
    profile_files = [f for f in get_profile_files(
    ) if not f.endswith("_description.txt")]
    return [os.path.basename(f)[:-4] for f in profile_files]


def get_content_from_file(filename, description=False):
    suffix = "_description" if description else ""
    filepath = os.path.join(PROFILE_DIR, f"{filename}{suffix}.txt")
    return read_file(filepath)


# *************************************************************
# Database functions

# Function to prepare text for database
def clean_text(text):
    # Define the replacments
    replacements = {
        'â€™': "'",
        'â€“': '—',
        'â€”': '—',
        'â€¦': '...'
    }
    # Replace
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def clear_db(db_filename="profiles.db"):
    conn = sqlite3.connect(db_filename)
    db_name = db_filename.split(".")[0]
    c = conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS {db_name}")
    conn.commit()
    conn.close()


def initialize_db(db_filename, schema):

    conn = sqlite3.connect(db_filename)
    db_name = db_filename.split(".")[0]
    c = conn.cursor()

    columns = ", ".join(f"{key} {value}" for key, value in schema.items())
    c.execute(f"CREATE TABLE IF NOT EXISTS {db_name} ({columns})")
    conn.commit()
    conn.close()


def update_db(db_filename="profiles.db", clear=False, schema=None):
    # Create a connection to the database
    conn = sqlite3.connect(db_filename)
    db_name = ".".split(db_filename)[0]

    # Create a cursor object
    c = conn.cursor()

    # *************************************************************
    if clear:
        # Drop the existing table
        c.execute(f"DROP TABLE IF EXISTS {db_filename}")
        conn.commit()
        # Recreate the table
        initialize_db(db_filename, schema)
    else:
        pass
    # *************************************************************

    # Populate the table with data
    for profile in get_filtered_file_list():
        name = clean_text(str(profile))
        description = clean_text(str(get_content_from_file(
            profile, description=True)))
        content = clean_text(str(get_content_from_file(
            profile, description=False)))
        try:
            c.execute("INSERT INTO profiles (name, description, content) VALUES (?, ?, ?)",
                      (name, description, content))
            conn.commit()  # Commit changes

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")

    c.execute("PRAGMA table_info(profiles)")
    columns = c.fetchall()
    for column in columns:
        print(column)

    # Once done with all operations, close the connection
    conn.close()


def add_profile_to_db(name, content, description):
    conn = sqlite3.connect('profiles.db')
    conn.execute("INSERT INTO profiles (name, content, description) VALUES (?, ?, ?)",
                 (name, content, description))
    conn.commit()
    conn.close()


def get_profile_list_from_db():
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('SELECT name FROM profiles')
    profile_names = [row[0] for row in c.fetchall()]
    conn.close()
    return profile_names


def get_profile_content_from_db(name):
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute("SELECT content FROM profiles WHERE name=?", (name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def get_profile_description_from_db(name):
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute("SELECT description FROM profiles WHERE name=?", (name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# *************************************************************
# Chat functions


# *************************************************************
if __name__ == "__main__":
    print("This is a library and is not meant to be run directly.")
