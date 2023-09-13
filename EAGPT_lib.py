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


def get_model_list(sort_choice):
    model_id_list = []
    for openai_model_dict in openai.Model.list()["data"]:
        model_id_list.append(openai_model_dict["id"])
    gpt_models = []
    for model in model_id_list:
        if model[0:3].lower() == "gpt":
            gpt_models.append(model)
        else:
            pass
    if sort_choice == True:
        gpt_models.sort()
        return gpt_models
    elif sort_choice == False:
        return gpt_models


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


def initialize_db(db_filename, schema):
    conn = sqlite3.connect(db_filename)
    db_name = db_filename.split(".")[0]
    c = conn.cursor()

    columns = ", ".join(f"{key} {value}" for key, value in schema.items())
    c.execute(f"CREATE TABLE IF NOT EXISTS {db_name} ({columns})")

    conn.commit()
    conn.close()


def update_db(db="profiles.db", clear=False, schema=None):
    # Create a connection to the database
    conn = sqlite3.connect(db)
    db_name = ".".split(db)[0]

    # Create a cursor object
    c = conn.cursor()

    # *************************************************************
    if clear:
        # Drop the existing table
        c.execute(f"DROP TABLE IF EXISTS {db}")
        # Recreate the table
        columns = ", ".join(f"{key} {value}" for key, value in schema.items())
        c.execute(f"CREATE TABLE IF NOT EXISTS {db_name} ({columns})")
        conn.commit()
    else:
        pass
    # *************************************************************

    # Populate the table with data
    for profile in get_filtered_file_list():
        name = clean_text(str(profile))
        description = clean_text(str(get_profile_content_from_file(
            profile, description=True)))
        content = clean_text(str(get_profile_content_from_file(
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


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


# *************************************************************
if __name__ == "__main__":
    print("This is a library and is not meant to be run directly.")
