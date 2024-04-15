# !pip install streamlit-card
import pandas as pd
from streamlit_card import card
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
import subprocess
import random
import streamlit as st  

session = st.session_state

from fetch import fetch_data, getlists

l = []

prompt = PromptTemplate(
    template="""{name}, a {age}-year-old {MBTI} from {State}, blends their love for {Hobby1} and {Hobby2} to express their creativity. Their introspective nature and appreciation for detail enrich their artistic pursuits, reflecting their cultural roots and passion for self-expression.""",
    input_variables=["name", "age","State","Hobby1","Hobby2","MBTI"],
)

from langchain_community.llms import Ollama 
llm = Ollama(model="tinyllama:1.1b-chat-v0.6-q4_1")
chain = prompt | llm

data = getlists()

import base64
def get_base64_encoded_image(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/jpeg;base64," + encoded.decode("utf-8")

import json

def save_username(username):
    with open("username.json", "w") as f:
        name = {"name": username}
        json.dump(name, f)  
    st.switch_page('pages/Chat.py')

for i in range(0, 10):
    name = data[0][i]
    age = data[1][i]
    gender = data[2][i]
    hobby1 = data[3][i]
    hobby2 = data[4][i]
    personality = data[5][i]
    state = data[6][i]

    name_dict = {"name": name}
    
    l = ["https://i.pinimg.com/736x/84/d3/32/84d3325978ce1b6845e466e501995509.jpg","https://png.pngtree.com/thumb_back/fh260/background/20221007/pngtree-aesthetic-red-background-image_1467120.jpg","https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3JtMjE4YmF0Y2g0LWF1bS0xOC5qcGc.jpg","https://png.pngtree.com/background/20211215/original/pngtree-aesthetic-background-pink-pastel-picture-image_1448496.jpg"]
    hasClicked = card(
    title=name,
    text= f"{name}, a {age}-year-old {personality} from {state}, blends their love for {hobby1} and {hobby2} to express their creativity. Their introspective nature and appreciation for detail enrich their artistic pursuits, reflecting their cultural roots and passion for self-expression.", 
    image=l[random.randint(0, len(l)-1)],
    key=i,
    styles={
        "card": {
                "width": "500px",
                "height": "500px",
            "border": "1px solid #ccc",
            "border-radius": "8px",
            "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"

        },
        "text": {
            "font-family": "Arial, sans-serif",
            "font-size": "16px"
        }
    },
    on_click = lambda : save_username(name)
    )
    l.append(hasClicked)
