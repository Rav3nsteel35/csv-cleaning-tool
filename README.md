# CSV Cleaning Tool

A Streamlit app that cleans messy CSV exports (duplicates, inconsistent
capitalization, phone number formats, missing values, stray whitespace) for
small businesses, restaurants, retail stores, researchers, and HR/office
staff who just need a clean CSV back out.

## Status

Early, incremental build. Current functionality: upload a CSV (or try the
bundled sample) and preview it. Cleaning steps are being added one at a
time — see `CLAUDE.md` for the full planned pipeline.

## Running locally

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Running tests

```bash
pytest
```

## Project layout

```
app.py            Streamlit UI only
cleaners/         One module per cleaning operation
utils/            Shared logic (CSV I/O, etc.)
tests/            pytest suite
sample_data/      Sample messy CSV for manual testing/demo
```
