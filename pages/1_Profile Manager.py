
import streamlit as st
import EAGPT_lib as eagpt
import json
from google.cloud import firestore
from google.oauth2 import service_account
import api_firebase as fb

st.title("Profile Manager")
st.markdown(
    '''
    Utility for managing, editing, and sharing system profiles.
    
    '''
)

key_dict = json.loads(st.secrets["firestore"]["db-key"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="eagpt-streamlit")

name = st.text_input("Enter profile name")
description = st.text_input("Enter profile description")
content = st.text_input("Enter profile content")
submit = st.button("Submit")

if name and description and content and submit:
    fb.set_db_value("profiles", name, "description", description)
    fb.set_db_value("profiles", name, "content", content)


profiles_ref = db.collection("profiles")
for doc in profiles_ref.stream():
    profile = doc.to_dict()
    name = doc.id
    description = profile["description"]

    st.subheader(f"Profile: {name}")
    st.write(f"Description: {description}")

# del_name = st.text_input("Enter profile name to delete")
# delete = st.button("Delete")

# if del_name and delete:
#     doc_ref = db.collection("profiles").document(del_name)
#     doc_ref.delete()


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
