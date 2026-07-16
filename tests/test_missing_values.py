import pandas as pd
import pytest

from cleaners.missing_values import handle_missing_values


def test_handle_missing_values_fill_replaces_and_counts():
    df = pd.DataFrame({"name": ["Alice", None], "city": [None, "Austin"]})

    result, count = handle_missing_values(df, strategy="fill", placeholder="N/A")

    assert count == 2
    assert list(result["name"]) == ["Alice", "N/A"]
    assert list(result["city"]) == ["N/A", "Austin"]


def test_handle_missing_values_drop_removes_rows_and_counts():
    df = pd.DataFrame({"name": ["Alice", None, "Bob"], "city": ["Chicago", "Austin", None]})

    result, count = handle_missing_values(df, strategy="drop")

    assert count == 2
    assert list(result["name"]) == ["Alice"]


def test_handle_missing_values_no_missing_data():
    df = pd.DataFrame({"name": ["Alice", "Bob"]})

    result, count = handle_missing_values(df, strategy="fill")

    assert count == 0
    assert list(result["name"]) == ["Alice", "Bob"]


def test_handle_missing_values_rejects_unknown_strategy():
    df = pd.DataFrame({"name": ["Alice"]})

    with pytest.raises(ValueError):
        handle_missing_values(df, strategy="guess")
