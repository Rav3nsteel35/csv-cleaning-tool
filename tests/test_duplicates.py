import pandas as pd

from cleaners.duplicates import remove_duplicates


def test_remove_duplicates_drops_exact_matches():
    df = pd.DataFrame(
        {
            "name": ["Alice", "Alice", "Bob"],
            "email": ["a@x.com", "a@x.com", "b@x.com"],
        }
    )

    result, count = remove_duplicates(df)

    assert count == 1
    assert result.shape[0] == 2
    assert list(result["name"]) == ["Alice", "Bob"]


def test_remove_duplicates_no_duplicates_present():
    df = pd.DataFrame({"name": ["Alice", "Bob"]})

    result, count = remove_duplicates(df)

    assert count == 0
    assert result.shape[0] == 2


def test_remove_duplicates_resets_index():
    df = pd.DataFrame({"name": ["Alice", "Alice", "Bob"]})

    result, _ = remove_duplicates(df)

    assert list(result.index) == [0, 1]
