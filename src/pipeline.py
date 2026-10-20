from pathlib import Path

from src.ingestion.fred import (
    fetch_fred_series,
    parse_fred_series,
)

from src.validation.macro_data import (
    validate_macro_series,
)

from src.database.repository import (
    upsert_observations,
)


def save_processed_data(
    df,
    series_id: str,
    output_dir: str = "data/processed",
) -> Path:
    """
    Save validated data to the processed layer.
    """

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = output_path / f"{series_id}.csv"

    df.to_csv(
        file_path,
        index=False,
    )

    print(
        f"[PROCESSING] Saved processed dataset to {file_path}"
    )

    return file_path


def run_series_pipeline(
    series_id: str,
) -> None:
    """
    Run the complete ingestion pipeline
    for one FRED series.
    """

    print(
        f"\n[PIPELINE] Starting {series_id}"
    )

    # 1. Extract raw data
    raw_file = fetch_fred_series(
        series_id
    )

    # 2. Parse into MacroLens standard schema
    df = parse_fred_series(
        raw_file,
        series_id,
    )

    # 3. Validate data quality
    validate_macro_series(df)

    # 4. Save processed file
    save_processed_data(
        df,
        series_id,
    )

    # 5. Persist to PostgreSQL
    rows_processed = upsert_observations(
        df
    )

    print(
        f"[DATABASE] Upserted {rows_processed} rows"
    )

    print(
        f"[PIPELINE] {series_id} completed"
    )


if __name__ == "__main__":
    run_series_pipeline(
        "CPIAUCSL"
    )