"""CSV loading utilities.

Small-business CSV exports (Excel, POS systems, HR software) are frequently
saved in cp1252/latin-1 rather than UTF-8, and are sometimes truncated or
not CSVs at all. This module centralizes the "make a best effort, then fail
loudly with a clear message" logic so app.py never has to deal with raw
pandas/encoding exceptions.
"""

import pandas as pd

# Encodings to attempt, in order. utf-8-sig handles BOM-prefixed files
# (common from Excel "CSV UTF-8" export), latin-1 never raises a
# UnicodeDecodeError so it's always the last resort.
_ENCODINGS_TO_TRY = ("utf-8-sig", "utf-8", "latin-1")


class CSVLoadError(Exception):
    """Raised when an uploaded file cannot be parsed as a CSV."""


def load_csv(uploaded_file) -> pd.DataFrame:
    """Parse a file-like object into a DataFrame.

    Args:
        uploaded_file: A file-like object supporting .seek() and .read(),
            such as Streamlit's UploadedFile.

    Returns:
        The parsed DataFrame.

    Raises:
        CSVLoadError: If the file is empty, not valid CSV, or unreadable
            under every encoding attempted.
    """
    last_error: Exception | None = None

    for encoding in _ENCODINGS_TO_TRY:
        try:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
        except pd.errors.EmptyDataError as exc:
            raise CSVLoadError("This file is empty.") from exc
        except pd.errors.ParserError as exc:
            raise CSVLoadError(
                "This file doesn't look like a valid CSV. Check that it's "
                "comma-separated and not corrupted."
            ) from exc

    raise CSVLoadError(
        "Couldn't read this file's text encoding. Try re-saving it as "
        "UTF-8 CSV and uploading again."
    ) from last_error
