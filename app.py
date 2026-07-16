"""CSV Cleaning Tool — Streamlit entry point.

This module is UI only: it wires up widgets and displays results. All
parsing/cleaning logic lives in utils/ and cleaners/ so it can be tested
without Streamlit.
"""

import streamlit as st

from cleaners.pipeline import CleaningOptions, run_pipeline
from utils.file_io import CSVLoadError, load_csv

SAMPLE_DATA_PATH = "sample_data/messy_sample.csv"

st.set_page_config(page_title="CSV Cleaning Tool", page_icon="🧹", layout="wide")

st.title("🧹 CSV Cleaning Tool")
st.write(
    "Upload a messy CSV export, choose cleaning options, preview the "
    "result, and download the cleaned file."
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

st.caption("No file handy?")
use_sample = st.button("Try it with sample data")

if use_sample:
    with open(SAMPLE_DATA_PATH, "rb") as f:
        st.session_state["df"] = load_csv(f)
    st.session_state["source_name"] = "messy_sample.csv (sample data)"
    st.session_state.pop("cleaned_df", None)
elif uploaded_file is not None:
    try:
        st.session_state["df"] = load_csv(uploaded_file)
        st.session_state["source_name"] = uploaded_file.name
        st.session_state.pop("cleaned_df", None)
    except CSVLoadError as e:
        st.error(str(e))
        st.session_state.pop("df", None)

if "df" in st.session_state:
    df = st.session_state["df"]
    columns = list(df.columns)

    st.subheader(f"Preview: {st.session_state['source_name']}")
    st.caption(f"{df.shape[0]} rows x {df.shape[1]} columns")
    st.dataframe(df, width="stretch")

    st.sidebar.header("Cleaning options")

    trim = st.sidebar.checkbox("Trim whitespace", value=True)

    cap_on = st.sidebar.checkbox("Standardize capitalization")
    cap_columns = (
        st.sidebar.multiselect("Columns to title-case", columns) if cap_on else []
    )

    phone_on = st.sidebar.checkbox("Standardize phone numbers")
    phone_column = (
        st.sidebar.selectbox("Phone column", columns) if phone_on else None
    )

    dedupe_on = st.sidebar.checkbox("Remove duplicate rows")

    missing_on = st.sidebar.checkbox("Handle missing values")
    missing_strategy = "fill"
    missing_placeholder = "N/A"
    if missing_on:
        missing_choice = st.sidebar.radio(
            "Missing value strategy",
            ["Fill with placeholder", "Drop incomplete rows"],
        )
        missing_strategy = "fill" if missing_choice == "Fill with placeholder" else "drop"
        if missing_strategy == "fill":
            missing_placeholder = st.sidebar.text_input("Placeholder text", value="N/A")

    if st.sidebar.button("Run cleaning", type="primary"):
        options = CleaningOptions(
            trim_whitespace=trim,
            standardize_capitalization=cap_on,
            capitalization_columns=cap_columns,
            standardize_phone=phone_on,
            phone_column=phone_column,
            remove_duplicates=dedupe_on,
            handle_missing=missing_on,
            missing_strategy=missing_strategy,
            missing_placeholder=missing_placeholder,
        )
        cleaned_df, summary = run_pipeline(df, options)
        st.session_state["cleaned_df"] = cleaned_df
        st.session_state["cleaning_summary"] = summary

    if "cleaned_df" in st.session_state:
        cleaned_df = st.session_state["cleaned_df"]
        summary = st.session_state["cleaning_summary"]

        st.subheader("Cleaned preview")
        messages = []
        if dedupe_on:
            messages.append(f"{summary.duplicates_removed} duplicate row(s) removed")
        if missing_on:
            noun = "row(s) dropped" if missing_strategy == "drop" else "value(s) filled"
            messages.append(f"{summary.missing_values_handled} missing {noun}")
        if messages:
            st.success(" · ".join(messages))

        st.caption(f"{cleaned_df.shape[0]} rows x {cleaned_df.shape[1]} columns")
        st.dataframe(cleaned_df, width="stretch")

        st.download_button(
            "Download cleaned CSV",
            data=cleaned_df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned.csv",
            mime="text/csv",
        )
