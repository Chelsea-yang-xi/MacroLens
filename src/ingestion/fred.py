from pathlib import Path
from datetime import datetime, timezone
import hashlib

import pandas as pd
import requests


FRED_BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


class FredIngestionError(Exception):
    """Raised when data cannot be ingested from FRED."""


def fetch_fred_series(
    series_id: str,
    raw_dir: str = "data/raw",
) -> Path:
    """
    Download a FRED time series and persist the unmodified raw CSV response.

    The function validates the upstream response before saving it so that
    HTML maintenance pages or other unexpected payloads are not stored as CSV.

    Parameters
    ----------
    series_id:
        FRED series identifier, e.g. CPIAUCSL.

    raw_dir:
        Directory where raw source files are stored.

    Returns
    -------
    Path
        Path of the saved raw CSV file.
    """

    raw_path = Path(raw_dir)
    raw_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    params = {
        "id": series_id,
    }

    try:
        response = requests.get(
            FRED_BASE_URL,
            params=params,
            timeout=30,
        )

        # Fail fast if FRED returns an HTTP error such as 404 or 500.
        response.raise_for_status()

    except requests.RequestException as exc:
        raise FredIngestionError(
            f"Failed to fetch FRED series '{series_id}'"
        ) from exc

    # HTTP 200 does not guarantee that the returned payload is valid data.
    # FRED may, for example, return an HTML maintenance page.
    content_type = response.headers.get(
        "Content-Type",
        "",
    )

    if "html" in content_type.lower():
        preview = response.text[:200].replace(
            "\n",
            " ",
        )

        raise FredIngestionError(
            f"FRED returned HTML instead of CSV "
            f"for series '{series_id}'. "
            f"The upstream service may be unavailable "
            f"or undergoing maintenance. "
            f"Response preview: {preview}"
        )

    response_text = response.text.lstrip()

    expected_header = (
        f"observation_date,{series_id}"
    )

    if not response_text.startswith(
        expected_header
    ):
        preview = response_text[:200].replace(
            "\n",
            " ",
        )

        raise FredIngestionError(
            f"Unexpected FRED response for "
            f"series '{series_id}'. "
            f"Expected CSV header "
            f"'{expected_header}', "
            f"but received: {preview}"
        )

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    filename = (
        f"{series_id}_{timestamp}.csv"
    )

    file_path = (
        raw_path / filename
    )

    # Preserve the exact upstream payload as the raw source of truth.
    file_path.write_bytes(
        response.content
    )

    # SHA-256 acts as a content fingerprint.
    # Later we can use it for duplicate detection or lineage checks.
    checksum = hashlib.sha256(
        response.content
    ).hexdigest()

    print(
        f"[INGESTION] Saved {series_id} "
        f"to {file_path}"
    )

    print(
        f"[INGESTION] SHA256: {checksum}"
    )

    return file_path


def parse_fred_series(
    raw_file: Path,
    series_id: str,
) -> pd.DataFrame:
    """
    Parse a raw FRED CSV into MacroLens' standard schema.
    """

    df = pd.read_csv(
        raw_file
    )

    expected_columns = {
        "observation_date",
        series_id,
    }

    missing_columns = (
        expected_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: "
            f"{missing_columns}"
        )

    df = df.rename(
        columns={
            "observation_date": "date",
            series_id: "value",
        }
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce",
    )

    df["series_id"] = series_id
    df["source"] = "FRED"

    # Store technical timestamps in UTC so local machine/server
    # timezone differences do not create ambiguity.
    df["ingested_at"] = datetime.now(
        timezone.utc
    )

    return df[
        [
            "date",
            "series_id",
            "value",
            "source",
            "ingested_at",
        ]
    ]