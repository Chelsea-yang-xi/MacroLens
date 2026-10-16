import pandas as pd


class DataValidationError(Exception):
    """Raised when macroeconomic data fails validation."""
#Data Quality Rules

def validate_macro_series(
    df: pd.DataFrame,
) -> None:
    """
    Validate the standard MacroLens time-series schema.
    """

    required_columns = {
        "date",
        "series_id",
        "value",
        "source",
        "ingested_at",
    }

    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise DataValidationError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    if df.empty:
        raise DataValidationError(
            "Dataset is empty"
        )

    if df["date"].isna().any():
        raise DataValidationError(
            "Dataset contains invalid dates"
        )

    if df["date"].duplicated().any():
        raise DataValidationError(
            "Dataset contains duplicate dates"
        )

    if not df["date"].is_monotonic_increasing:
        raise DataValidationError(
            "Dates must be sorted "
            "in ascending order"
        )

    missing_ratio = df["value"].isna().mean()

    if missing_ratio > 0.05:
        raise DataValidationError(
            f"Too many missing values: "
            f"{missing_ratio:.2%}"
        )