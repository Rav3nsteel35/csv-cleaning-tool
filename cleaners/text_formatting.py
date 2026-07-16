"""Capitalization standardization for selected text columns."""

import pandas as pd


def standardize_capitalization(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to title case (e.g. "JOHN SMITH" -> "John Smith").

    Only the given columns are touched; email/notes-style free text is left
    alone unless explicitly selected. Missing values pass through unchanged.

    Known limitation: Python's title-case rules capitalize the letter after
    every apostrophe, so possessives like "mcdonald's" become "Mcdonald'S"
    instead of "Mcdonald's". Names like "O'Connor" are handled correctly;
    possessive apostrophes are the known edge case.

    Args:
        df: Input DataFrame.
        columns: Column names to standardize. Columns not present in df
            are ignored.

    Returns:
        A new DataFrame with the selected columns title-cased.
    """
    result = df.copy()

    for column in columns:
        if column in result.columns:
            result[column] = result[column].str.title()

    return result
