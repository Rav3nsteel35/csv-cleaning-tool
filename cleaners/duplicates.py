"""Duplicate row removal."""

import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Drop exact full-row duplicates, keeping the first occurrence.

    Args:
        df: Input DataFrame.

    Returns:
        A tuple of (deduplicated DataFrame, number of rows removed).
        Run this after whitespace/capitalization/phone standardization so
        rows that only differ by formatting are recognized as duplicates.
    """
    duplicate_count = int(df.duplicated().sum())
    result = df.drop_duplicates().reset_index(drop=True)

    return result, duplicate_count
