import pandas as pd

from cleaners.whitespace import trim_whitespace


def test_trim_whitespace_strips_leading_and_trailing():
    df = pd.DataFrame({"name": [" Alice ", "Bob  ", "  Carl"]})

    result = trim_whitespace(df)

    assert list(result["name"]) == ["Alice", "Bob", "Carl"]


def test_trim_whitespace_leaves_numeric_columns_untouched():
    df = pd.DataFrame({"age": [30, 25]})

    result = trim_whitespace(df)

    assert list(result["age"]) == [30, 25]


def test_trim_whitespace_preserves_missing_values():
    df = pd.DataFrame({"name": [" Alice ", None]})

    result = trim_whitespace(df)

    assert result["name"][0] == "Alice"
    assert pd.isna(result["name"][1])
