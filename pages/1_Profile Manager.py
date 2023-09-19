
import streamlit as st
from sqlalchemy import text
import EAGPT_lib as eagpt

st.title("Profile Manager")
st.markdown(
    '''
    Utility for managing, editing, and sharing system profiles.
    
    '''
)

# Deprecated SQL workflow

# profile_schema = {
#     "name": "TEXT PRIMARY KEY",
#     "content": "TEXT",
#     "description": "TEXT"
# }

# eagpt.update_db(db_filename="profiles.db", clear=True, schema=profile_schema)

# if st.button("Clear DB"):
#     eagpt.clear_db(db_filename="profiles.db")

# input = st.text_input("Enter profile name")

# if st.button("Add profile"):
#     eagpt.add_profile_to_db(
#         name=input,
#         description=input,
#         content=input
#     )

# conn2 = st.experimental_connection('profiles_db', type='sql')
# profiles = conn2.query('select * from profiles')
# st.dataframe(profiles)
