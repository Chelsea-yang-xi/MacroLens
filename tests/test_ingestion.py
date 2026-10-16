import pandas as pd
import pytest

from src.validation.macro_data import (
    validate_macro_series,
    DataValidationError,
)


def create_valid_dataframe():

    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2025-01-01",
                    "2025-02-01",
                    "2025-03-01",
                ]
            ),
            "series_id": [
                "TEST",
                "TEST",
                "TEST",
            ],
            "value": [
                100.0,
                101.0,
                102.0,
            ],
            "source": [
                "TEST",
                "TEST",
                "TEST",
            ],
            "ingested_at": pd.to_datetime(
                [
                    "2026-01-01",
                    "2026-01-01",
                    "2026-01-01",
                ]
            ),
        }
    )


def test_valid_macro_series_passes():

    df = create_valid_dataframe()

    validate_macro_series(df)


def test_duplicate_dates_fail():

    df = create_valid_dataframe()

    df.loc[1, "date"] = df.loc[0, "date"]

    with pytest.raises(
        DataValidationError
    ):
        validate_macro_series(df)