import sqlite3
import EAGPT_lib as eagpt
import streamlit as st


# # Create a connection to the database
# conn = sqlite3.connect('profiles.db')

# # Create a cursor object
# c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE profiles
#              (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# # Insert ten rows of data
# names = ['John', 'Sarah', 'Mike', 'Emma', 'David',
#          'Sophia', 'Daniel', 'Olivia', 'James', 'Isabella']
# ages = [23, 27, 30, 22, 25, 28, 31, 24, 26, 29]

# for i in range(10):
#     c.execute("INSERT INTO profiles VALUES (?, ?, ?)", (i, names[i], ages[i]))

# # Save (commit) the changes
# conn.commit()

# # Close the connection
# conn.close()

# *************************************************************
print("\n")

# Create a connection to the database
conn = sqlite3.connect('profiles.db')

# Create a cursor object
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS profiles (name TEXT PRIMARY KEY, description TEXT, content TEXT)''')

for profile in eagpt.get_filtered_profile_list():
    name = str(profile)
    description = str(eagpt.get_profile_content_from_file(
        profile, description=True))
    content = str(eagpt.get_profile_content_from_file(
        profile, description=False))
    try:
        c.execute("INSERT INTO profiles VALUES (?, ?, ?)",
                  (name, description, content))
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        # print(f"name: {name}, description: {description}, content: {content}")

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()
