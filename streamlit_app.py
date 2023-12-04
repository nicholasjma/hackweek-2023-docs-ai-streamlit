import json
import os

import streamlit as st
import streamlit_scrollable_textbox as stx
import requests

from streamlit.logger import get_logger

logger = get_logger(__name__)
st.title("Iterable RAG Demo")

url = "https://hackweek-2023-docs-ai-54bd3e77ac5b.herokuapp.com/query"
username = os.environ["API_USERNAME"]
password = os.environ["API_PASSWORD"]


def generate_response(input_text):
    r = requests.get(url, auth=(username, password), json={"query": input_text})
    logger.info(r.status_code)
    response = r.json()
    logger.info(r.status_code, response)
    stx.scrollable_textbox(response["result"])
    stx.scrollable_textbox(json.dumps(response))


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "How do I build a churn model using predictive goals? How would I create a campaign to "
        "target likely to churn users?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
