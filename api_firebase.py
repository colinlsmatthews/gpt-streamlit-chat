import streamlit as st
import EAGPT_lib as eagpt
import json
from google.cloud import firestore
from google.oauth2 import service_account


key_dict = json.loads(st.secrets["firestore"]["db-key"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="eagpt-streamlit")


def set_db_value(collection, document, field, value):
    doc_ref = db.collection(collection).document(document)
    doc_ref.update({field: value})


def get_db_value(collection, document, field):
    doc_ref = db.collection(collection).document(document)
    doc = doc_ref.get()
    return doc.to_dict()[field]


def get_db_document(collection, document):
    doc_ref = db.collection(collection).document(document)
    doc = doc_ref.get()
    return doc.to_dict()


def get_db_document_list(collection, sort=None, reverse=False):
    docs = db.collection(collection).stream()
    doc_list = []
    for doc in docs:
        doc_list.append(doc.id)
    if sort:
        doc_list.sort(key=lambda x: x[sort], reverse=reverse)
    return doc_list
