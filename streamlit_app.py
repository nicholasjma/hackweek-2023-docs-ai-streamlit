import json
import os

import streamlit as st
import streamlit_scrollable_textbox as stx
import requests

from streamlit.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(layout="wide")
st.title("Iterable RAG Demo")

url = "https://hackweek-2023-docs-ai-54bd3e77ac5b.herokuapp.com/query"
username = os.environ["API_USERNAME"]
password = os.environ["API_PASSWORD"]


def generate_response(input_text):
    r = requests.get(url, auth=(username, password), json={"query": input_text})
    logger.info(r.status_code)
    response = r.json()
    logger.info(r.status_code, response)
    markdown = response["result"]
    markdown += "\n\n## Sources\n\n"
    for n, source in enumerate(response["sources"], start=1):
        markdown += f"{n}. [{source['page_title']}]({source['url']})\n\n"
    st.write(markdown)
    st.write("## Search Results"\n\n")
    for n, search_result in enumerate(response["search_results"], start=1):
        st.write(f" {n}. {search_result['page_title']}")
        st.write(search_result["page_content"][:20])

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "How do I build a churn model using predictive goals? How would I create a campaign to "
        "target likely to churn users?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
