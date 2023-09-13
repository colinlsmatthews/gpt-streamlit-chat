
import streamlit as st
from sqlalchemy import text
import EAGPT_lib as eagpt

profile_schema = {
    "name": "TEXT PRIMARY KEY",
    "content": "TEXT",
    "description": "TEXT"
}


eagpt.update_db(db_filename="profiles.db", clear=True, schema=profile_schema)

# Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.experimental_connection('pets_db', type='sql')

# # Insert some data with conn.session.
# with conn.session as s:
#     t1 = text('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);')
#     s.execute(t1)
#     t2 = text('DELETE FROM pet_owners;')
#     s.execute(t2)
#     pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
#     for k in pet_owners:
#         t3 = text('INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);')
#         s.execute(t3, params=dict(owner=k, pet=pet_owners[k]))
#     s.commit()

# # Query and display the data you inserted
# pet_owners = conn.query('select * from pet_owners')
# st.dataframe(pet_owners)

if st.button("Clear DB"):
    eagpt.clear_db(db_filename="profiles.db")

input = st.text_input("Enter profile name")

if st.button("Add profile"):
    eagpt.add_profile_to_db(
        name=input,
        description=input,
        content=input
    )

conn2 = st.experimental_connection('profiles_db', type='sql')
profiles = conn2.query('select * from profiles')
st.dataframe(profiles)
