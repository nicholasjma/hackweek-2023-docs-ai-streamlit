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

st.image(
    "https://iterable.com/wp-content/uploads/2020/02/Iterable_Logo_01.gif", width=200
)

url = "https://hackweek-2023-docs-ai-54bd3e77ac5b.herokuapp.com/query"
username = os.environ["API_USERNAME"]
password = os.environ["API_PASSWORD"]


def trim_to_space(s: str, max_len: int = 400):
    if len(s) < max_len:
        return s
    else:
        return s[:max_len].rsplit(" ", 1)[0] + "..."


def generate_response(input_text):
    with st.spinner(text="Reticulating splines...", cache=False):
        r = requests.get(url, auth=(username, password), json={"query": input_text})
    response = r.json()
    container = st.container(border=True)
    markdown = response["result"]
    markdown += "\n\n## Sources\n\n"
    for n, source in enumerate(response["sources"], start=1):
        markdown += f"{n}. [{source['page_title']}]({source['url']})\n\n"
    container.write(markdown)
    container2 = st.container(border=True)
    container2.write("## Search Results\n\n")
    for n, search_result in enumerate(response["search_results"], start=1):
        st.write(
            f" {n}. (score {search_result['score']:.2f}) [{search_result['page_title']}]({search_result['source']})"
        )
        st.write(search_result["page_content"][:400])
    time.sleep(1)
    container.write("## a")


with st.form("my_form"):
    text = st.text_area(
        "How can Iterable assist you today?",
        "How do I build a churn model using predictive goals? How would I create a campaign to "
        "target likely to churn users?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
