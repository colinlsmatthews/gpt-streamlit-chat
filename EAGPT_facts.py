# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import os
import openai
import tiktoken
import tkinter as tk


#declare global variables
openai.organization = "org-VQ8Slx5WR2WUeXOCdbA68dqR" #Ennead org

if os.getenv("OPENAI_API_KEY_ENNEAD"):
    openai.api_key = os.getenv("OPENAI_API_KEY_ENNEAD")
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")

user = os.getlogin()
MODEL = "gpt-3.5-turbo-16k"
TEMP = 0
PROFILE = "profile_facts.txt"
with open(PROFILE, 'r') as file:
    profile = file.read()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print ("\n\nSystem prompt: FACTS")
    print(f'Hi, {name}! \nYou are chatting with GPT-3.5 using a system prompt designed for Ennead Architects. \nThe prompt prioritizes listing facts about the firm.')  # Press Ctrl+F8 to toggle the breakpoint.

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
    user_input = input("Write a prompt (type \"exit\" to end conversation)\n_____________________________________\n\n")
    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)

    if user_input.lower() == 'exit':
        print("Ending the conversation.")
        return

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi(user)

#print(completion("text-davinci-003", "Say this is a test", 7, 0))

messages = [
    {"role": "system",
     "content": "You are a marketing coordinator for an architecture firm with the following profile: {}".format(
         profile)}
]
#print(openai.Model.list())
chat(messages)
