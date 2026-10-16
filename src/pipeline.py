from pathlib import Path

from src.ingestion.fred import (
    fetch_fred_series,
    parse_fred_series,
)

from src.validation.macro_data import (
    validate_macro_series,
)

#Orchestration
def save_processed_data(
    df,
    series_id: str,
    output_dir: str = "data/processed",
) -> Path:

    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        output_path /
        f"{series_id}.csv"
    )

    df.to_csv(
        file_path,
        index=False,
    )

    print(
        f"[PROCESSING] Saved processed "
        f"dataset to {file_path}"
    )

    return file_path


def run_series_pipeline(
    series_id: str,
) -> None:

    print(
        f"\n[PIPELINE] Starting {series_id}"
    )

    raw_file = fetch_fred_series(
        series_id
    )

    df = parse_fred_series(
        raw_file,
        series_id,
    )

    validate_macro_series(df)

    save_processed_data(
        df,
        series_id,
    )

    print(
        f"[PIPELINE] {series_id} completed"
    )


if __name__ == "__main__":

    run_series_pipeline(
        "CPIAUCSL"
    )