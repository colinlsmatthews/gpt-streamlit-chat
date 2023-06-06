# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import os
import openai

#declare global variables
openai.organization = "org-VQ8Slx5WR2WUeXOCdbA68dqR"
openai.api_key = os.getenv("OPENAI_API_KEY_ENNEAD")
user = os.getlogin()
MODEL = "gpt-3.5-turbo"
TEMP = 0
with open('profile.txt', 'r') as file:
    profile = file.read()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def completion(_model, _prompt, _max_tokens, _temperature):
    return openai.Completion.create(
        model = _model,
        prompt = _prompt,
        max_tokens = _max_tokens,
        temperature = _temperature
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi(user)

#print(completion("text-davinci-003", "Say this is a test", 7, 0))

messages = [
    {"role": "system",
     "content": "You are a marketing coordinator for an architecture firm with the following profile: {}".format(
         profile)}
]
def run(messages):
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
        #print(messages)

    except ValueError:
        print("Invalid input. Please enter a text prompt.")

    run(messages)

run(messages)
