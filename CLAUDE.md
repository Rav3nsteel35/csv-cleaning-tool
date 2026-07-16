# CSV Cleaning Tool

## Project Goal

Build a professional Streamlit application that cleans messy CSV files for small businesses.

This project is intended to be a portfolio-quality software engineering project demonstrating:
- Python
- Pandas
- Streamlit
- Data Cleaning
- Modular Software Design

The application should solve real business problems rather than exist as a coding demo.

---

## Target Users

- Small businesses
- Restaurants
- Retail stores
- Researchers
- HR departments
- Office staff

---

## Core Features

Current pipeline:

1. Upload CSV
2. Preview original data
3. Remove duplicates
4. Standardize capitalization
5. Standardize phone numbers
6. Handle missing values
7. Trim whitespace
8. Preview cleaned data
9. Download cleaned CSV

Future features may include:
- Date normalization
- Address cleaning
- Email validation
- Custom cleaning rules
- Cleaning reports
- Batch processing

---

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly (future)
- Git

---

## Development Philosophy

- Build incrementally.
- Never generate the entire project at once.
- Prefer small commits.
- Keep functions focused on one responsibility.
- Favor readability over cleverness.
- Follow Python best practices.
- Add docstrings to public functions.
- Explain architectural decisions before implementing them.

---

## Code Organization

Separate responsibilities whenever possible.

Example:

app.py
cleaners/
utils/
tests/
sample_data/
assets/

Avoid putting all logic into app.py.

---

## UI Principles

The interface should feel simple enough for a non-technical business owner.

Users should be able to:

Upload
↓

Preview
↓

Choose cleaning options
↓

Run cleaning
↓

Preview results
↓

Download cleaned CSV

Keep the interface clean and intuitive.

---

## Collaboration Rules

Act as a senior software engineer.

Before implementing major features:
- Explain the design.
- Point out tradeoffs.
- Recommend best practices.

If you think there is a better architectural approach than the one requested, explain why before coding.

Do not rewrite unrelated code unless necessary.

Keep responses concise and focused.