import streamlit as st
import requests

# Sidebar for API Key input
st.sidebar.title("Chatbot Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password", value=st.session_state.get("api_key", ""))

# Clear API Key button
if st.sidebar.button("Clear API Key"):
    # Clear the API Key from session state and reset input form
    st.session_state.api_key = ""  # Clear the API Key from session state
    st.session_state.messages = []  # Optionally clear the chat history too
    st.rerun()  # Refresh the page to reset the form and state
# Clear Chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.rerun() 
# Main Chat Title
st.title("Hi I'm Chatbot")

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history (All user messages on left, bot replies on right)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])



# User input
user_input = st.chat_input("Message SushilGPT")

if user_input:
    if not api_key:
        st.sidebar.warning("Please enter an API key!")  # Show warning if API key is missing
    else:
        # Save the API Key in session state so that it persists across interactions
        st.session_state.api_key = api_key
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Send request to Flask API
        response = requests.post(
            "http://127.0.0.1:5000/chat",
            json={"message": user_input, "api_key": api_key},
        )

        # Check API response
        if response.status_code == 200:
           
            bot_reply = response.json().get("reply", "Error: No response")
        elif response.status_code == 401:
            bot_reply = "Invalid API Key. Please enter a valid API key!"
            st.sidebar.error(bot_reply)  # Show error message for invalid API key
        else:
            # Handle other errors (e.g., server errors)
            bot_reply = f"Error: {response.status_code} - {response.text}"

        # Append the bot's reply to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

