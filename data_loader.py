from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "equity_us", "equity_nl",
    "cpi_us", "cpi_nl",
    "ip_us", "ip_nl",
    "unemp_us", "unemp_nl",
    "rate_us", "rate_nl",
}

def load_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = (
        df.sort_values("date")
          .drop_duplicates("date")
          .reset_index(drop=True)
    )

    if df["date"].isna().any():
        raise ValueError("Invalid date values found.")

    return df
