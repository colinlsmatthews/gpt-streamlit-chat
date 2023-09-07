import os
import openai
import tiktoken
import glob
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

def get_profile_list():
    profile_files = []
    files = glob.glob(os.path.join(".\profiles\\", "*.txt"))
    for file in files:
        if file[-15::] == "description.txt":
            pass
        else:
            profile_files.append(file)
    items = []
    for file in profile_files:
        filename = file.split("\\")[-1]
        items.append(filename[0:-4])
    result = [item for item in items if item is not None]
    return result

def get_profile_description(filename):
    filepath = ".\profiles\\" + filename + "_description.txt"
    files = glob.glob(os.path.join(".\profiles\\", "*.txt"))
    if filepath in files:
        with open(filepath, "r") as file:
            contents = file.read()
            return contents
    else:
        pass

def get_profile_text(filename):
    filepath = ".\profiles\\" + filename + ".txt"
    files = glob.glob(os.path.join(".\profiles\\", "*.txt"))
    if filepath in files:
        with open(filepath, "r") as file:
            contents = file.read()
            return contents
    else:
        pass

# *************************************************************
# Chat functions

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
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
    pass