# CSV Cleaning Tool

A Streamlit app that cleans messy CSV exports (duplicates, inconsistent
capitalization, phone number formats, missing values, stray whitespace) for
small businesses, restaurants, retail stores, researchers, and HR/office
staff who just need a clean CSV back out.

## Status

The core pipeline from `CLAUDE.md` is implemented: upload (or try the
bundled sample) → preview → choose cleaning options → run → preview
cleaned data → download. Future features listed in `CLAUDE.md` (date
normalization, address cleaning, email validation, cleaning reports,
batch processing) are not yet started.

### Cleaning options

- **Trim whitespace** — strips leading/trailing whitespace from every text column.
- **Standardize capitalization** — title-cases selected columns.
- **Standardize phone numbers** — reformats a selected column to `(XXX) XXX-XXXX`; values that don't reduce to exactly 10 US digits are left untouched rather than guessed at.
- **Remove duplicate rows** — drops exact full-row duplicates.
- **Handle missing values** — either fill with a placeholder (default `N/A`) or drop incomplete rows. No statistical imputation (mean/mode) is offered: guessing a missing name or phone number from statistics would be misleading for this kind of data.

These steps always run in a fixed order — trim → capitalize → standardize
phone → dedupe → missing values — regardless of the order you enable them
in the sidebar. This matters: standardizing case/formatting before
deduplication lets rows that only differ by casing (`"JOHN SMITH"` vs.
`"John Smith"`) be recognized as duplicates. See `cleaners/pipeline.py`.

### Known limitations

- Title-casing mishandles possessives: `"mcdonald's"` becomes `"Mcdonald'S"` instead of `"Mcdonald's"`. Names like `"O'Connor"` are handled correctly; possessive apostrophes are the edge case.
- Duplicate detection is full-row only. Two rows that are clearly the same person but differ in a free-text column (e.g. one has a `Notes` entry and the other doesn't) are intentionally left as separate rows, not merged or fuzzy-matched.

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
