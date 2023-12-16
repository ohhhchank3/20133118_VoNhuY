import openai
import streamlit as st
from streamlit_chat import message

# Setting page title and header
st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>CHATBOT - TLCN 😬</h1>", unsafe_allow_html=True)

import ham_fake as Chat

# Set org ID and API key
openai.organization = "<YOUR_OPENAI_ORG_ID>"
openai.api_key = "<YOUR_OPENAI_API_KEY>"

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []

# Sidebar - let user choose model and let user clear the current conversation
st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['total_tokens'] = []

def generate_response1(prompt):
    answer = Chat.get_last_message_content(prompt)
    return answer

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response1(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(f"Model used: {st.session_state['model_name'][i]}")
