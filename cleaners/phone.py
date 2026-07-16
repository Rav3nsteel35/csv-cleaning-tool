"""Phone number standardization."""

import re

import pandas as pd

_NON_DIGIT = re.compile(r"\D")


def _format_phone(value):
    if pd.isna(value):
        return value

    digits = _NON_DIGIT.sub("", str(value))

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        # Can't confidently reformat a number that isn't 10 US digits
        # after stripping a country code - leave it as-is rather than
        # mangle it or guess.
        return value

    return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"


def standardize_phone_numbers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Reformat US phone numbers in the given column to "(XXX) XXX-XXXX".

    Args:
        df: Input DataFrame.
        column: Name of the column containing phone numbers.

    Returns:
        A new DataFrame with the column reformatted. Values that don't
        reduce to exactly 10 digits (after optionally stripping a leading
        "1" country code) are left unchanged rather than guessed at.
    """
    result = df.copy()

    if column in result.columns:
        result[column] = result[column].apply(_format_phone)

    return result
