import pandas as pd
import pytest

from src.features import log_change, build_features

def test_log_change_is_positive_when_series_rises():
    s = pd.Series([100.0, 105.0, 110.0])
    result = log_change(s)
    assert result.iloc[1] > 0

def test_log_change_rejects_zero():
    s = pd.Series([100.0, 0.0, 110.0])
    with pytest.raises(ValueError):
        log_change(s)

def test_build_features_contains_target():
    df = pd.DataFrame({
        "date": pd.date_range("2020-01-01", periods=12, freq="MS"),
        "equity_us": range(100, 112),
        "cpi_us": range(200, 212),
        "ip_us": range(300, 312),
        "unemp_us": [5.0] * 12,
        "rate_us": [1.0] * 12,
    })
    result = build_features(df, "us")
    assert "next_month_equity_return" in result.columns
