import pandas as pd

from cleaners.phone import standardize_phone_numbers


def test_standardize_phone_numbers_handles_mixed_formats():
    df = pd.DataFrame(
        {
            "phone": [
                "(555) 123-4567",
                "555-987-6543",
                "555.987.6543",
                "5551122334",
                "555 234 5566",
            ]
        }
    )

    result = standardize_phone_numbers(df, "phone")

    assert list(result["phone"]) == [
        "(555) 123-4567",
        "(555) 987-6543",
        "(555) 987-6543",
        "(555) 112-2334",
        "(555) 234-5566",
    ]


def test_standardize_phone_numbers_strips_leading_country_code():
    df = pd.DataFrame({"phone": ["1-555-123-4567"]})

    result = standardize_phone_numbers(df, "phone")

    assert result["phone"][0] == "(555) 123-4567"


def test_standardize_phone_numbers_leaves_unparseable_untouched():
    df = pd.DataFrame({"phone": ["555-1234", "call the office", ""]})

    result = standardize_phone_numbers(df, "phone")

    assert list(result["phone"]) == ["555-1234", "call the office", ""]


def test_standardize_phone_numbers_preserves_missing_values():
    df = pd.DataFrame({"phone": ["(555) 123-4567", None]})

    result = standardize_phone_numbers(df, "phone")

    assert pd.isna(result["phone"][1])
