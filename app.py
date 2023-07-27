import streamlit as st
import urllib
import os
import time
import requests
import random
import base64
from data import (speech_text, get_answer, text_speech) 

from components.sidebar import sidebar

#changes
def clear_submit():
    st.session_state["submit"] = False

#################

st.set_page_config(page_title="GenAI Smart Search", page_icon="📖", layout="wide")
st.header("GenAI Smart Search Engine")

sidebar()

with st.expander("Instructions"):
    st.markdown("""
                Ask a question that you think can be answered with the information trained with GenerativeAI
                """)
text1 = "Which date does cricket world cup start"
text2 = "What are the Gen AI use-cases that are applicable to Data engineering, that you can service"
text3 = "How do you differentiate between Automation and Generative AI use-cases"

options = [text1,text2,text3]

prompt_text = st.text_input("Enter the prompt:", value= """ Write a few words about Generative AI from Google? """
, on_change=clear_submit)


col1, col2 = st.columns([1,2])
with col1:
    generate = st.button('Generate Response')
with col2:
    selected_question = st.selectbox('Select the questions:', options, index=0)

if generate or st.session_state.get("submit"):
    if not selected_question or not prompt_text:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        # Output Columns
        placeholder = st.empty()
        if prompt_text:
            input = speech_text(prompt_text)
        else:
            input = speech_text(selected_question)

        answer = get_answer(input)

        file_path=text_speech(answer)
            
        def autoplay_audio(file_path: str):
            with open(file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                    <audio controls autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                st.markdown(
                    md,
                    unsafe_allow_html=True,
                    )

        with placeholder.container():
            st.markdown("# Auto-playing Audio!")
            try: 
                autoplay_audio("local_audio.mp3")
            
            except:
                st.markdown("N/A")
                st.markdown("---")
                st.markdown("#### Search Results")
