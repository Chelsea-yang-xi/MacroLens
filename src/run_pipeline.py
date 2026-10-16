from pathlib import Path
import pandas as pd

from data_loader import load_data
from features import build_features
from analysis import correlation_matrix, fit_baseline

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_macro_data.csv"
OUTPUT_DIR = ROOT / "outputs"

def run_country(df, country: str):
    features = build_features(df, country)

    corr = correlation_matrix(features)
    _, metrics, coefficients, predictions = fit_baseline(features)

    corr.to_csv(OUTPUT_DIR / f"{country}_correlation_matrix.csv")
    coefficients.to_csv(
        OUTPUT_DIR / f"{country}_feature_coefficients.csv",
        index=False
    )
    predictions.to_csv(
        OUTPUT_DIR / f"{country}_predictions.csv",
        index=False
    )

    metrics_row = {"country": country, **metrics}
    return metrics_row

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_data(DATA_PATH)

    results = [
        run_country(df, "us"),
        run_country(df, "nl"),
    ]

    metrics = pd.DataFrame(results)
    metrics.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)

    print("\nBaseline model metrics")
    print(metrics.to_string(index=False))
    print("\nOutputs saved to:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
