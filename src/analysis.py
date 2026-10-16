import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURES = [
    "inflation",
    "ip_growth",
    "interest_rate_change",
    "unemployment_change",
    "inflation_lag_1",
    "equity_return_lag_1",
    "rolling_volatility_6m",
]

TARGET = "next_month_equity_return"

def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    columns = FEATURES + [TARGET]
    return df[columns].corr()

def time_split(df: pd.DataFrame, train_ratio: float = 0.8):
    split_idx = int(len(df) * train_ratio)
    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()
    return train, test

def fit_baseline(df: pd.DataFrame):
    train, test = time_split(df)

    X_train = train[FEATURES]
    y_train = train[TARGET]
    X_test = test[FEATURES]
    y_test = test[TARGET]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": np.sqrt(mean_squared_error(y_test, predictions)),
        "r2": r2_score(y_test, predictions),
        "train_rows": len(train),
        "test_rows": len(test),
    }

    coefficients = pd.DataFrame({
        "feature": FEATURES,
        "coefficient": model.coef_,
    }).sort_values("coefficient", key=lambda s: s.abs(), ascending=False)

    prediction_frame = test[["date", TARGET]].copy()
    prediction_frame["prediction"] = predictions

    return model, metrics, coefficients, prediction_frame
