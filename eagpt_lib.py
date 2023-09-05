import os
import openai
import tiktoken
import glob

# global variables
MODEL = "gpt-4"
TEMP = 0.5
PROFILE = "default"
profile_directory = ".\profiles\\" + PROFILE + ".txt"
with open(profile_directory, 'r') as f:
    profile = f.read()

# functions
