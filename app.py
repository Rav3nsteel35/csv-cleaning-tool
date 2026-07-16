"""CSV Cleaning Tool — Streamlit entry point.

This module is UI only: it wires up widgets and displays results. All
parsing/cleaning logic lives in utils/ and cleaners/ so it can be tested
without Streamlit.
"""

import streamlit as st

from utils.file_io import CSVLoadError, load_csv

SAMPLE_DATA_PATH = "sample_data/messy_sample.csv"

st.set_page_config(page_title="CSV Cleaning Tool", page_icon="🧹", layout="wide")

st.title("🧹 CSV Cleaning Tool")
st.write(
    "Upload a messy CSV export and preview it below. Cleaning options "
    "(duplicates, formatting, missing values) are coming in the next steps."
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

st.caption("No file handy?")
use_sample = st.button("Try it with sample data")

if use_sample:
    with open(SAMPLE_DATA_PATH, "rb") as f:
        st.session_state["df"] = load_csv(f)
    st.session_state["source_name"] = "messy_sample.csv (sample data)"
elif uploaded_file is not None:
    try:
        st.session_state["df"] = load_csv(uploaded_file)
        st.session_state["source_name"] = uploaded_file.name
    except CSVLoadError as e:
        st.error(str(e))
        st.session_state.pop("df", None)

if "df" in st.session_state:
    df = st.session_state["df"]
    st.subheader(f"Preview: {st.session_state['source_name']}")
    st.caption(f"{df.shape[0]} rows x {df.shape[1]} columns")
    st.dataframe(df, width="stretch")
