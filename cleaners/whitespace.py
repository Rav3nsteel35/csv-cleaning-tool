"""Whitespace trimming."""

import pandas as pd


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from every text (object) column.

    Args:
        df: Input DataFrame.

    Returns:
        A new DataFrame with text cells stripped. Non-text columns are
        left untouched.
    """
    result = df.copy()
    text_columns = result.select_dtypes(include=["object", "string"]).columns

    for column in text_columns:
        result[column] = result[column].str.strip()

    return result
