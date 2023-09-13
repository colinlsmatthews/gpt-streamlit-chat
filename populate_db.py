import sqlite3
import EAGPT_lib as eagpt
import streamlit as st


# Create a connection to the database
conn = sqlite3.connect('profiles.db')

# Create a cursor object
c = conn.cursor()

# *************************************************************
# Drop the existing table
c.execute("DROP TABLE IF EXISTS profiles")

# Recreate the table with the new structure
c.execute('''CREATE TABLE profiles
             (id INTEGER PRIMARY KEY,
              name TEXT, 
              description TEXT, 
              content TEXT)''')

# commit the transaction
conn.commit()
# *************************************************************

# Populate the table with data
for profile in eagpt.get_filtered_profile_list():
    name = str(profile)
    description = str(eagpt.get_profile_content_from_file(
        profile, description=True))
    content = str(eagpt.get_profile_content_from_file(
        profile, description=False))
    try:
        c.execute("INSERT INTO profiles (name, description, content) VALUES (?, ?, ?)",
                  (name.encode('utf-8'), description.encode('utf-8'), content.encode('utf-8')))
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        # print(f"name: {name}, description: {description}, content: {content}")

# names = ["name1", "name2", "name3"]
# descriptions = ["description1", "description2", "description3"]
# contents = ["content1", "content2", "content3"]

# # Zip the lists together
# data_tuples = list(zip(names, descriptions, contents))

# for name, description, content in data_tuples:
#     try:
#         c.execute("INSERT INTO profiles (name, description, content) VALUES (?, ?, ?)",
#                   (name, description, content))
#         # Since no error occurred, commit this transaction
#         conn.commit()
#     except sqlite3.IntegrityError as e:
#         print(f"IntegrityError: {e}")
#         print(f"name: {name}, description: {description}, content: {content}")

c.execute("PRAGMA table_info(profiles)")
columns = c.fetchall()
for column in columns:
    print(column)


# Once done with all operations, close the connection
conn.close()
