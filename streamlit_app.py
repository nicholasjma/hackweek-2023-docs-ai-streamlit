import json
import os

import streamlit as st
import requests

st.title("Iterable RAG Demo")

url = "https://hackweek-2023-docs-ai-54bd3e77ac5b.herokuapp.com/query"
username = os.environ["API_USERNAME"]
password = os.environ["API_PASSWORD"]


def generate_response(input_text):
    r = requests.get(url, auth=(username, password), json={"query": input_text})
    response = r.json()
    st.text(response["result"])
    st.text(json.dumps(response))


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "How do I build a churn model using predictive goals? How would I create a campaign to "
        "target likely to churn users?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
