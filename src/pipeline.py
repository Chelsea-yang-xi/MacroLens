from pathlib import Path

from src.ingestion.fred import (
    fetch_fred_series,
    parse_fred_series,
)

from src.validation.macro_data import (
    validate_macro_series,
)

from src.validation.data_quality import (
    calculate_data_quality,
)

from src.database.repository import (
    upsert_observations,
    save_quality_result,
    start_pipeline_run,
    complete_pipeline_run,
    fail_pipeline_run,
)


SERIES_CONFIG = {
    "CPIAUCSL": "Consumer Price Index",
    "UNRATE": "Unemployment Rate",
    "FEDFUNDS": "Federal Funds Rate",
    "INDPRO": "Industrial Production Index",
}


def save_processed_data(
    df,
    series_id: str,
    output_dir: str = "data/processed",
) -> Path:
    """
    Save validated data to the processed data layer.
    """

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        output_path
        / f"{series_id}.csv"
    )

    df.to_csv(
        file_path,
        index=False,
    )

    print(
        f"[PROCESSING] "
        f"Saved processed dataset to "
        f"{file_path}"
    )

    return file_path


def run_series_pipeline(
    series_id: str,
) -> None:
    """
    Run the complete ingestion and data-quality pipeline
    for one macroeconomic time series.

    A failure is recorded in PostgreSQL and then re-raised
    so the higher-level batch runner can decide whether to
    continue processing other series.
    """

    print(
        f"\n[PIPELINE] "
        f"Starting {series_id}"
    )

    run_id = start_pipeline_run(
        series_id
    )

    try:
        # 1. Extract raw data from FRED
        raw_file = fetch_fred_series(
            series_id
        )

        # 2. Parse into MacroLens standard schema
        df = parse_fred_series(
            raw_file,
            series_id,
        )

        # 3. Validate required schema and basic data quality
        validate_macro_series(
            df
        )

        # 4. Calculate data-quality metrics
        quality_result = (
            calculate_data_quality(
                df,
                series_id,
            )
        )

        # 5. Save quality result for monitoring/dashboard
        save_quality_result(
            quality_result
        )

        # 6. Save validated dataset to processed layer
        save_processed_data(
            df,
            series_id,
        )

        # 7. Persist observations to PostgreSQL
        rows_processed = (
            upsert_observations(
                df
            )
        )

        # 8. Mark pipeline run as successful
        complete_pipeline_run(
            run_id,
            rows_processed,
        )

        print(
            f"[QUALITY] "
            f"{series_id}: "
            f"{quality_result.status}"
        )

        print(
            f"[DATABASE] "
            f"Upserted "
            f"{rows_processed} rows"
        )

        print(
            f"[PIPELINE] "
            f"{series_id} completed"
        )

    except Exception as exc:
        fail_pipeline_run(
            run_id
        )

        print(
            f"[PIPELINE] "
            f"{series_id} FAILED: "
            f"{exc}"
        )

        # Re-raise so the batch runner knows
        # this individual series failed.
        raise


def run_all_series() -> None:
    """
    Run the pipeline for all configured macroeconomic series.

    Failures are isolated per series so one upstream or
    processing failure does not stop the entire batch.
    """

    failed_series = []

    successful_series = []

    for (
        series_id,
        series_name,
    ) in SERIES_CONFIG.items():

        print(
            f"\n=== "
            f"{series_name} "
            f"({series_id}) "
            f"==="
        )

        try:
            run_series_pipeline(
                series_id
            )

            successful_series.append(
                series_id
            )

        except Exception as exc:
            failed_series.append(
                series_id
            )

            print(
                f"[PIPELINE] "
                f"Continuing after "
                f"{series_id} failure: "
                f"{exc}"
            )

    print(
        "\n============================"
    )

    print(
        "[PIPELINE] Run summary"
    )

    print(
        "============================"
    )

    if successful_series:
        print(
            f"[PIPELINE] "
            f"Successful series: "
            f"{', '.join(successful_series)}"
        )
    else:
        print(
            "[PIPELINE] "
            "No series completed successfully"
        )

    if failed_series:
        print(
            f"[PIPELINE] "
            f"Failed series: "
            f"{', '.join(failed_series)}"
        )
    else:
        print(
            "[PIPELINE] "
            "No failed series"
        )

    print(
        "============================"
    )


if __name__ == "__main__":
    run_all_series()