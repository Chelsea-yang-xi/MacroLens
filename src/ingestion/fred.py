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
    Download a FRED time series and persist the unmodified raw response.

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
    raw_path.mkdir(parents=True, exist_ok=True)

    params = {
        "id": series_id
    }

    try:
        response = requests.get(
            FRED_BASE_URL,
            params=params,
            timeout=30,  #alow a 30 seconds timeout to wait resilence 
        )

        response.raise_for_status()  #fail fast 

    except requests.RequestException as exc:
        raise FredIngestionError(
            f"Failed to fetch FRED series '{series_id}'" #abstraction
        ) from exc

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    filename = f"{series_id}_{timestamp}.csv" #Data lineage
    file_path = raw_path / filename

    file_path.write_bytes(response.content) #save the raw

    checksum = hashlib.sha256(   #idempotency
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

    df = pd.read_csv(raw_file)

    expected_columns = {
        "observation_date",
        series_id,
    }

    missing_columns = (
        expected_columns - set(df.columns)
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

    df["ingested_at"] = datetime.now(
        timezone.utc  #store timestamps in UTC
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