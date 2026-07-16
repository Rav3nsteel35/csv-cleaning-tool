import io

import pytest

from utils.file_io import CSVLoadError, load_csv


def test_load_csv_good_path():
    csv_bytes = io.BytesIO(b"name,age\nAlice,30\nBob,25\n")

    df = load_csv(csv_bytes)

    assert list(df.columns) == ["name", "age"]
    assert df.shape == (2, 2)


def test_load_csv_falls_back_to_latin1():
    # 'é' encoded as latin-1 is a byte sequence that is invalid UTF-8,
    # so the utf-8 attempts must fail before latin-1 succeeds.
    csv_bytes = io.BytesIO("name,city\nRene,Montreal city: caf\xe9\n".encode("latin-1"))

    df = load_csv(csv_bytes)

    assert df.shape == (1, 2)
    assert "café" in df.loc[0, "city"]


def test_load_csv_empty_file_raises():
    csv_bytes = io.BytesIO(b"")

    with pytest.raises(CSVLoadError):
        load_csv(csv_bytes)
