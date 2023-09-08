import streamlit as st
import openai
import numpy as np
import random
import time
import re
import EAGPT_lib as eagpt

st.title("EAGPT")
st.divider()
st.sidebar.markdown("# Settings")

# Get API key
api_toggle = st.sidebar.toggle(
    "Manual API key input",
    value=False,
    help="Use manual API key input to override the API key stored in Streamlit secrets."
)

api_key_input = st.sidebar.text_input(
    "OpenAI API Key",
    type="default",
    help="You can find your API key at https://platform.openai.com/account",
    placeholder="sk-...",
    disabled=not api_toggle
)

if not api_toggle:
    api_key_input = st.secrets["OPENAI_API_KEY"]

# Set API key

try:
    openai.api_key = api_key_input
    eagpt.get_model_list(True)
    st.sidebar.markdown("*OpenAI API key successfully set!*")
    model_auth = True
except Exception as e:
    model_auth = False
    if "Invalid authorization header" in str(e):
        st.sidebar.markdown("*Authentication failed: no key provided*")
    elif "Incorrect API key provided" in str(e):
        st.sidebar.markdown("*Authentication failed: invalid key*")
    else:
        st.sidebar.markdown(f"*Authentication failed: {e}*")

if model_auth:
    # Set temperature
    st.session_state["openai_temp"] = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.5,
        step=0.1,
        format="%.1f",
        help="Please enter new temperature between 0 and 2. "
        "Lower values for temperature result in more consistent outputs, "
        "while higher values generate more diverse and creative results. "
        "Select a temperature value based on the desired trade-off between "
        "coherence and creativity for your specific application."
    )

    # Get model selection
    st.session_state["openai_model"] = st.sidebar.selectbox(
        "Model Selection",
        eagpt.get_model_list(True),
        help="Please select a model from the dropdown menu."
    )

    # Set profile
    profile = st.sidebar.selectbox(
        "Profile Selection",
        eagpt.get_profile_list(),
        index=eagpt.get_profile_list().index("default"),
        help="Please select a profile from the dropdown menu."
    )

    st.sidebar.markdown("### Profile Description:")
    st.sidebar.markdown(f"*{eagpt.get_profile_description(profile)}*")

    start_chat = st.sidebar.button(
        "Start new chat",
        type="primary",
        use_container_width=True
    )

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": f"{eagpt.get_profile_text(profile)}"}
        ]
    if start_chat:
        st.session_state["messages"] = [
            {"role": "system", "content": f"{eagpt.get_profile_text(profile)}"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if not message["role"] == "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Is there life on Mars?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    temperature=st.session_state["openai_temp"],
                    messages=[{"role": m["role"], "content": m["content"]}
                              for m in st.session_state.messages],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get(
                        "content", "")
                    message_placeholder.markdown(full_response + "▌")

            except Exception as e:
                error_message = str(e)
                match = re.search(
                    r"This model's maximum context length is (\d+) tokens\. However, your messages resulted in (\d+) tokens\. Please reduce the length of the messages\.", error_message)
                if match:
                    # Group 0 is the entire match
                    formatted_message = match.group(0)
                    st.error(formatted_message)
                else:
                    st.error(f"An unexpected error occurred: {e}")

            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
else:
    pass
