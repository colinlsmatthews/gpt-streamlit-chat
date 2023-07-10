import os
import openai
import tiktoken
import glob
import tkinter as tk

#**************************************************
#global variables
MODEL = "gpt-3.5-turbo-16k"
TEMP = 0.5
PROFILE = "default"
profile_directory = ".\profiles\\" + PROFILE + ".txt"
with open(profile_directory, 'r') as file:
    profile = file.read()

#**************************************************
#functions
def print_hi(name):
    print(f'Hi, {name}! Welcome to EAGPT')

def key_authentication():
    env_var_type = input("\nAre you using an Ennead key? (Y/N)\n").upper()
    if env_var_type == "Y":
        print("\nAuthenticating with the following environment variables:\n\"OPENAI_API_KEY_ENNEAD\"\n\"OPENAI_ORG_ENNEAD\"")
        openai.organization = os.getenv("OPENAI_ORG_ENNEAD")
        openai.api_key = os.getenv("OPENAI_API_KEY_ENNEAD")
    elif env_var_type == "N":
        print("\nAuthenticating with the following environment variables:\n\"OPENAI_API_KEY_PERSONAL\"\n\"OPENAI_ORG_PERSONAL\"")
        openai.organization = os.getenv("OPENAI_ORG_PERSONAL")
        openai.api_key = os.getenv("OPENAI_API_KEY_PERSONAL")
    else:
        print("\nInvalid input. Please reenter.")
        key_authentication()

def manual_authentication():
    openai.organization = input("\nPlease enter your OpenAI organization ID:\n")
    openai.api_key = input("\nPlease enter your OpenAI API key:\n")

def authenticate():
    auth_choice = input("\nDo you wish to authenticate using environment variables? (Y/N)\n").upper()

    if auth_choice == "Y":
        key_authentication()
    elif auth_choice == "N":
        manual_authentication()
    else:
        print("\nInvalid input. Please reenter.")
        authenticate()


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


def get_model():
    global MODEL
    model_choice = input(f"\nThe current model is \"{MODEL}\". Would you like to change? (Y/N)\n").upper()
    if model_choice == "Y":
        display_models = input("\nWould you like to see a list of available chat models? (Y/N)\n").upper()
        if display_models == "Y":
            for model in get_model_list(True):
                print(model)
            new_model = input("\nInput new model name. Type \"cancel\" to keep default.\n").lower()
            if new_model != "cancel":
                MODEL = new_model
                print(f"\nThe model has been changed to \"{new_model}\"")
            elif new_model == "cancel":
                pass
        elif display_models == "N":
            new_model = input("\nInput new model name. Type \"cancel\" to keep default.\n").lower()
            if new_model != "cancel":
                MODEL = new_model
                print(f"\nThe model has been changed to \"{new_model}\"")
            elif new_model == "cancel":
                pass
        else:
            print("\nInvalid input. Please reenter.")
            get_model()
    elif model_choice == "N":
        pass

def get_temp():
    global TEMP
    temp_choice = input(f"\nThe current model temperature is {TEMP}. Would you like to change? (Y/N)\n").upper()
    if temp_choice == "Y":
        new_temp = float(input("\nPlease enter new temperature between 0 and 2. "
                             "Lower values for temperature result in more consistent outputs, "
                             "while higher values generate more diverse and creative results. "
                             "Select a temperature value based on the desired trade-off between "
                             "coherence and creativity for your specific application.\n"))
        TEMP = new_temp
        print(f"\nTemperature set to {TEMP}.\n")
    elif temp_choice == "N":
        pass
    else:
        print("\nInvalid input. Please reenter.")
        get_temp()

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

def get_profile(initial_call = True):
    global PROFILE

    if initial_call:
        profile_choice = input(f"\nThe current profile is \"{PROFILE}\" Would you like to change? (Y/N)\n").upper()
    else:
        profile_choice = "Y"

    if profile_choice == "Y":
        print("\nAvailable profiles:\n")
        for item in get_profile_list():
            print(item)
        new_profile = input("\nInput new profile name. Type \"cancel\" to keep default.\n").lower()
        if new_profile != "cancel":
            PROFILE = new_profile
            get_profile_description(new_profile)
            accept_choice = input("\nKeep choice? (Y/N)\n").upper()
            if accept_choice == "Y":
                print(f"\nThe profile has been changed to \"{new_profile}\"")
            else:
                get_profile(False)
        elif new_profile == "cancel":
            pass
    elif profile_choice == "N":
        pass
    else:
        print("\nInvalid input. Please reenter.")
        get_profile(True)

def completion(_model, _prompt, _max_tokens, _temperature):
    return openai.Completion.create(
        model = _model,
        prompt = _prompt,
        max_tokens = _max_tokens,
        temperature = _temperature
    )
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

def chat(messages):
    print("_____________________________________")
    user_input = input("Write a prompt (type \"exit\" to end conversation, "
                       "\"model\" to change models, "
                       "\"temp\" to change the temperature,"
                       "and \"profile\" to change the system profile."
                       "\n_____________________________________\n\n")
    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)

    if user_input.lower() == 'exit':
        print("Ending the conversation.")
        return

    elif user_input.lower() == "model":
        get_model()

    elif user_input.lower() == "temp":
        get_temp()

    elif user_input.lower() == "profile":
        get_profile()

    try:
        response = openai.ChatCompletion.create(
            model = MODEL,
            messages = messages,
            temperature = TEMP
        )
        print(response['choices'][0]['message']['content'])
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']
        gpt_message = {"role": f"{role}", "content": f"{content}" }
        messages.append(gpt_message)
        num_tokens = num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
        print(f"Number of tokens used: {num_tokens}")
        #print(messages) #uncomment to reveal message history for testing

    except ValueError:
        print("Invalid input. Please enter a text prompt.")

    chat(messages)


#**************************************************
#script

if __name__ == '__main__':
    print_hi(os.getlogin())

    authenticate()

    get_model()

    get_temp()

    get_profile()

    messages = [
        {"role": "system",
         "content": "You are a marketing coordinator for an architecture firm with the following profile: {}".format(profile)}
    ]

    chat(messages)
