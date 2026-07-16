"""Missing value handling.

Deliberately does not offer statistical imputation (mean/median/mode).
This tool targets business records (names, emails, phone numbers) where a
guessed value is misleading rather than useful - the safe choices are to
either drop the incomplete row or flag it with a visible placeholder for a
human to fix.
"""

import pandas as pd

VALID_STRATEGIES = ("drop", "fill")


def handle_missing_values(
    df: pd.DataFrame, strategy: str = "fill", placeholder: str = "N/A"
) -> tuple[pd.DataFrame, int]:
    """Drop or fill rows/cells containing missing values.

    Args:
        df: Input DataFrame.
        strategy: "drop" removes any row with at least one missing value.
            "fill" replaces missing cells with `placeholder`.
        placeholder: Text used when strategy is "fill".

    Returns:
        A tuple of (resulting DataFrame, count of rows dropped or cells
        filled, depending on strategy).

    Raises:
        ValueError: If strategy is not "drop" or "fill".
    """
    if strategy not in VALID_STRATEGIES:
        raise ValueError(f"strategy must be one of {VALID_STRATEGIES}, got {strategy!r}")

    if strategy == "drop":
        rows_with_missing = df.isna().any(axis=1)
        count = int(rows_with_missing.sum())
        result = df[~rows_with_missing].reset_index(drop=True)
        return result, count

    count = int(df.isna().sum().sum())
    result = df.fillna(placeholder)
    return result, count
