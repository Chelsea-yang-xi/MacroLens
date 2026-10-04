import numpy as np
import pandas as pd

def log_change(series: pd.Series) -> pd.Series:
    if (series <= 0).any():
        raise ValueError("Log-change inputs must be strictly positive.")
    return np.log(series / series.shift(1))

def build_features(df: pd.DataFrame, country: str) -> pd.DataFrame:
    if country not in {"us", "nl"}:
        raise ValueError("country must be 'us' or 'nl'")

    out = pd.DataFrame({"date": df["date"]})

    out["equity_return"] = log_change(df[f"equity_{country}"])
    out["inflation"] = log_change(df[f"cpi_{country}"])
    out["ip_growth"] = log_change(df[f"ip_{country}"])
    out["interest_rate_change"] = df[f"rate_{country}"].diff()
    out["unemployment_change"] = df[f"unemp_{country}"].diff()

    out["inflation_lag_1"] = out["inflation"].shift(1)
    out["equity_return_lag_1"] = out["equity_return"].shift(1)
    out["rolling_volatility_6m"] = out["equity_return"].rolling(6).std()

    out["next_month_equity_return"] = out["equity_return"].shift(-1)

    return out.dropna().reset_index(drop=True)
