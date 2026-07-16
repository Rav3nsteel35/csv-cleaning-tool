"""Pipeline orchestration.

Cleaning steps are not independent: standardizing text/phone formatting
before deduplication lets rows that only differ by casing or formatting
be recognized as duplicates, and trimming whitespace has to happen before
any of that for the same reason. This module owns that ordering so it
lives in one tested place instead of being implicit in UI code.
"""

from dataclasses import dataclass, field

import pandas as pd

from cleaners.duplicates import remove_duplicates
from cleaners.missing_values import handle_missing_values
from cleaners.phone import standardize_phone_numbers
from cleaners.text_formatting import standardize_capitalization
from cleaners.whitespace import trim_whitespace


@dataclass
class CleaningOptions:
    trim_whitespace: bool = False
    standardize_capitalization: bool = False
    capitalization_columns: list[str] = field(default_factory=list)
    standardize_phone: bool = False
    phone_column: str | None = None
    remove_duplicates: bool = False
    handle_missing: bool = False
    missing_strategy: str = "fill"
    missing_placeholder: str = "N/A"


@dataclass
class CleaningSummary:
    duplicates_removed: int = 0
    missing_values_handled: int = 0


def run_pipeline(df: pd.DataFrame, options: CleaningOptions) -> tuple[pd.DataFrame, CleaningSummary]:
    """Run the enabled cleaning steps in a fixed, correctness-preserving order.

    Order: trim whitespace -> standardize capitalization -> standardize
    phone -> remove duplicates -> handle missing values. Steps not enabled
    in `options` are skipped, but enabled steps always run in this order
    regardless of the order they were set.

    Args:
        df: Input DataFrame.
        options: Which steps to run and their parameters.

    Returns:
        A tuple of (cleaned DataFrame, summary of counts affected).
    """
    result = df.copy()
    summary = CleaningSummary()

    if options.trim_whitespace:
        result = trim_whitespace(result)

    if options.standardize_capitalization and options.capitalization_columns:
        result = standardize_capitalization(result, options.capitalization_columns)

    if options.standardize_phone and options.phone_column:
        result = standardize_phone_numbers(result, options.phone_column)

    if options.remove_duplicates:
        result, summary.duplicates_removed = remove_duplicates(result)

    if options.handle_missing:
        result, summary.missing_values_handled = handle_missing_values(
            result, options.missing_strategy, options.missing_placeholder
        )

    return result, summary
