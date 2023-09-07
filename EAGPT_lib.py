import os
import openai
import tiktoken
import glob
import streamlit as st

# if "api_key" in st.session_state:
#     openai.api_key = st.session_state["api_key"]

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
            print("\n" + contents)
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





if __name__ == "__main__":
    pass