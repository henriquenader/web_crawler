
import streamlit as st
import pandas as pd
import numpy as np
import datetime





st.set_page_config(
    page_title="Início",
    page_icon="👋",
)

st.write("# Welcome to WebCrawler! 👋")

# st.sidebar.success("Select a demo above.")

st.markdown(
    """

    ### How to use:
    - Insert the kind of job you want to search.
    - Insert the location.
    - Use the slider to choose the radius.
    - Click the RUN button.
    - The table will appear, but you can download it clicking on the DOWNLOAD button.

"""
)