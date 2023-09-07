import streamlit as st
import numpy as np
import random
import time

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

st.title("EAGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    assistant_response = random.choice(
        [
            "I'm doing great, thanks for asking!",
            "I'm doing well, thanks for asking!",
            "I'm doing okay, thanks for asking!",
            "I'm doing poorly, thanks for asking!",
            "I'm doing terribly, thanks for asking!",
        ]
    )
    # Simulate stream of respose with milliseconds of delay
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": full_response})