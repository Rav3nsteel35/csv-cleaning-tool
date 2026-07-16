import pandas as pd

from cleaners.pipeline import CleaningOptions, run_pipeline


def _case_duplicate_df():
    return pd.DataFrame(
        {
            "name": ["JOHN SMITH", "John Smith"],
            "phone": ["(555) 123-4567", "(555) 123-4567"],
            "city": ["Chicago", "Chicago"],
        }
    )


def test_pipeline_no_options_returns_df_unchanged():
    df = pd.DataFrame({"name": [" Alice ", "BOB"]})

    result, summary = run_pipeline(df, CleaningOptions())

    assert list(result["name"]) == [" Alice ", "BOB"]
    assert summary.duplicates_removed == 0
    assert summary.missing_values_handled == 0


def test_pipeline_capitalization_before_dedupe_catches_case_duplicates():
    df = _case_duplicate_df()
    options = CleaningOptions(
        standardize_capitalization=True,
        capitalization_columns=["name"],
        remove_duplicates=True,
    )

    result, summary = run_pipeline(df, options)

    assert summary.duplicates_removed == 1
    assert result.shape[0] == 1
    assert result["name"][0] == "John Smith"


def test_pipeline_dedupe_without_capitalization_misses_case_duplicates():
    # Demonstrates why ordering matters: without standardizing case first,
    # these two rows still look different and neither gets removed.
    df = _case_duplicate_df()
    options = CleaningOptions(remove_duplicates=True)

    result, summary = run_pipeline(df, options)

    assert summary.duplicates_removed == 0
    assert result.shape[0] == 2


def test_pipeline_full_run_applies_all_enabled_steps():
    df = pd.DataFrame(
        {
            "name": [" JOHN SMITH", "John Smith "],
            "phone": ["555-123-4567", "(555) 123-4567"],
            "notes": [None, None],
        }
    )
    options = CleaningOptions(
        trim_whitespace=True,
        standardize_capitalization=True,
        capitalization_columns=["name"],
        standardize_phone=True,
        phone_column="phone",
        remove_duplicates=True,
        handle_missing=True,
        missing_strategy="fill",
        missing_placeholder="N/A",
    )

    result, summary = run_pipeline(df, options)

    assert result.shape[0] == 1
    assert result["name"][0] == "John Smith"
    assert result["phone"][0] == "(555) 123-4567"
    assert result["notes"][0] == "N/A"
    assert summary.duplicates_removed == 1
    assert summary.missing_values_handled == 1
