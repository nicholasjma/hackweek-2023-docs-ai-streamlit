import os
import time

import streamlit as st
import requests

from streamlit.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(layout="wide")

# Remove whitespace from the top of the page and sidebar
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


url = "https://hackweek-2023-docs-ai-54bd3e77ac5b.herokuapp.com/query"
# username = os.environ["API_USERNAME"]
# password = os.environ["API_PASSWORD"]


def trim_to_space(s: str, max_len: int = 400):
    if len(s) < max_len:
        return s
    else:
        return s[:max_len].rsplit(" ", 1)[0] + "..."


def generate_response(input_text):
    with st.spinner(text="Reticulating splines...", cache=False):
        r = requests.get(
            url, auth=(username, password), json={"query": input_text}, timeout=120
        )
    logger.info(r.status_code)
    logger.info(r.raw)
    response = r.json()
    container = st.container(border=True)
    markdown = response["result"]
    if response["sources"]:
        markdown += "\n\n*Sources*\n\n"
    for n, source in enumerate(response["sources"], start=1):
        markdown += f"[{source['pageTitle']}]({source['source']})  \n"
    container.write(markdown)
    with st.expander("Search Results", expanded=False):
        for n, search_result in enumerate(response["searchResults"], start=1):
            st.write(
                f"{n}. (score {search_result['score']:.2f}) (origin {search_result.get('origin')}) [{search_result['pageTitle']}]({search_result['source']})"
            )
            st.write(search_result["pageContent"][:400])


st.image(
    "https://iterable.com/wp-content/uploads/2020/02/Iterable_Logo_01.gif",
    width=75,
)
with st.form("my_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    text = st.text_area(
        "How can Iterable assist you today?",
        "How do I build a churn model using predictive goals? How would I create a campaign to "
        "target likely to churn users?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
