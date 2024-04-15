import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import google.generativeai as genai
import time
import ollama
from langchain_openai import OpenAI
import os 


llm = OpenAI(openai_api_key='')


import json

# load username

nn = ''
with open("username.json", "r") as f:
    username = json.load(f)
    nn = username["name"]

import hashlib
def generate_salt():
    return str(os.urandom(16).hex())

def hash_message(message, salt):
    return str(hashlib.sha256(salt.encode() + message.encode()).hexdigest())

def save_to_json(encoded_msg,hash, filename):
    if(os.path.exists(filename)):
        with open(filename, "r") as f:
            data = json.load(f)
            if f"DHRUV" not in data:
                data[f"DHRUV"] = {}
            else:
                if f"{nn}" not in data[f"DHRUV"]:
                    data[f"DHRUV"][f"{nn}"] = []

                else:
                    data[f"DHRUV"][f"{nn}"].append([encoded_msg,hash])
            
        with open(filename, "w") as f:
            json.dump(data, f)

    else:
        data = {}
        if f"DHRUV" not in data: 
            data[f"DHRUV"] = {}

        else:
            if f"{nn}" not in data[f"DHRUV"]:
                data[f"DHRUV"][f"{nn}"] = []
            else:
                    data[f"DHRUV"][f"{nn}"].append([encoded_msg,hash])
        with open(filename, 'w') as f:
            json.dump(data, f)




# Load authorization token from file
try:
    with open("token.json", "r") as f:
        token_file = json.load(f)
        token = token_file["token"]
except FileNotFoundError:
    print("Error: Please Sign In first !")
    exit(1)

from query import fetch_fitness_data

fit_data = fetch_fitness_data(token)

st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_page_config(page_title="Advisor", page_icon="🤖", layout="wide")
# st.set_page_config(layout="wide")

# Streamed response emulator
def response_generator(prompt):
    text = ollama.chat(
    model='medllama2',
    messages=[{'role': 'user', 'content': prompt}],
    stream=False
    )
    text = llm(prompt)
    salt = generate_salt()
    encoded_msg = hash_message(text, str(salt))
    try:
        save_to_json(encoded_msg, hash, "data.json")
    except:
        print("Error in encryption")
    for word in text.split():
        yield word + " "
        time.sleep(0.05)


# Left-aligned greeting using Markdown and HTML
def colored_markdown(text: str, color: str):
    return f'<p class="title" style="background-color: #fff; color: {color}; padding: 5px; line-height: 1">{text}</p>'

sidebar = st.sidebar

# Greeting with custom colors
st.markdown(colored_markdown(f"{nn}", "#007bff"),
            unsafe_allow_html=True)  # Blue color
#st.markdown(colored_markdown(f"{nn}?", "#39A5A9"),
#            unsafe_allow_html=True)  # Red color

st.markdown(
    """
    <style>
        .title {
            text-align: left; 
            font-size: 60px;
            margin-bottom: 0px;
            padding-bottom: 5px;
            display: inline-block;  
        }
        .subtitle {
            text-align: left;
            font-size: 24px;
            color: #333333; 
            margin-top: 5px; 
        }
        .square-container {
            display: flex;
            flex-wrap: wrap;
        }
        .square {
            width: 150px;
            height: 150px;
            background-color: #36A5A9;
            margin: 10px;
            margin-top: 30px;  
            margin-bottom: 50px;  
            color: #ffffff;
            padding: 10px;
            text-align: left;
            font-size: 14px;
            line-height: 1.5;
            border-radius: 16px;
            position: relative;  /* Enable relative positioning for image */
        }
        .square-image {
            position: absolute;  /* Make image absolute within square */
            bottom: 5px;  /* Position image at bottom */
            right: 5px;  /* Position image at right */
            width: 20px;
            height: 20px;
        }
        .input-container {
            display: flex;
            align-items: center;
            position: relative;
            margin-top: 20px;
        }
        .input-text {
            flex: 1;
            height: 40px;
            padding: 10px;
            font-size: 16px;
            border-radius: 12px;
            border: 1px solid #ccc;
            margin-right: 10px;
        }
        .button-container {
            display: flex;
            gap: 0px;
        }
        .button {
            
            height: 40px;
            width: 40px;
            margin: 0px;
            padding: 0px;
            display: flex;
            justify-content: center;
            align-items: center;
            # background-color: #39A5A9;
            color: #fff;
            border-radius: 8px;
            cursor: pointer;
        }
        .button svg {
            width: 24px;
            height: 24px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.write("##")
st.sidebar.markdown("<h2 style='text-align: center;'>User Dashboard</h2>", unsafe_allow_html=True)
st.sidebar.write("##")
