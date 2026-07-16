import pandas as pd

from cleaners.text_formatting import standardize_capitalization


def test_standardize_capitalization_title_cases_selected_column():
    df = pd.DataFrame({"name": ["JOHN SMITH", "maria garcia"], "email": ["JOHN@X.COM", "m@x.com"]})

    result = standardize_capitalization(df, ["name"])

    assert list(result["name"]) == ["John Smith", "Maria Garcia"]
    # Untouched: email wasn't in the selected columns.
    assert list(result["email"]) == ["JOHN@X.COM", "m@x.com"]


def test_standardize_capitalization_handles_apostrophes():
    df = pd.DataFrame({"name": ["sarah o'connor"]})

    result = standardize_capitalization(df, ["name"])

    assert result["name"][0] == "Sarah O'Connor"


def test_standardize_capitalization_ignores_unknown_columns():
    df = pd.DataFrame({"name": ["john smith"]})

    result = standardize_capitalization(df, ["not_a_column"])

    assert list(result["name"]) == ["john smith"]


def test_standardize_capitalization_preserves_missing_values():
    df = pd.DataFrame({"name": ["john smith", None]})

    result = standardize_capitalization(df, ["name"])

    assert result["name"][0] == "John Smith"
    assert pd.isna(result["name"][1])
