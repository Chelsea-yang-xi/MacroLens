# MacroLens
### Macroeconomic Data Analysis & Baseline Predictive Modelling

**Version 0.1 — beginner portfolio release**

MacroLens is a small data science project exploring how macroeconomic indicators relate to equity-market returns in the United States and the Netherlands.

The first release deliberately keeps the modelling simple. The goal is to show a clean end-to-end workflow before adding more advanced models later.

## What this version demonstrates

- data loading and validation
- time-series feature engineering
- exploratory data analysis
- correlation analysis
- a baseline Linear Regression model
- train/test splitting that respects time order
- MAE, RMSE and R² evaluation
- reproducible project structure
- basic automated tests

## Research question

> How are inflation, interest rates, unemployment and industrial production associated with equity-market returns, and how well can a simple baseline model predict the next month's return?

This is a **data science learning project**, not an investment strategy.

---

## Project structure

```text
MacroLens/
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── requirements.txt
├── data/
│   └── sample_macro_data.csv
├── src/
│   ├── data_loader.py
│   ├── features.py
│   ├── analysis.py
│   └── run_pipeline.py
├── tests/
│   └── test_features.py
└── outputs/
    ├── correlation_matrix.csv
    ├── model_metrics.csv
    └── feature_coefficients.csv
```

---

## Dataset

The repository currently contains a **synthetic monthly demo dataset** so the project can run immediately.

Columns include:

| Variable | Description |
|---|---|
| `equity_us` / `equity_nl` | equity price index |
| `cpi_us` / `cpi_nl` | consumer price index |
| `ip_us` / `ip_nl` | industrial production index |
| `unemp_us` / `unemp_nl` | unemployment rate |
| `rate_us` / `rate_nl` | interest rate |

The next version will replace the demo data with documented public data sources.

---

## Feature engineering

For each country, the pipeline creates:

- monthly equity return
- monthly inflation
- industrial production growth
- monthly interest-rate change
- monthly unemployment change
- 1-month lagged inflation
- 1-month lagged equity return
- 6-month rolling equity volatility

The prediction target is:

```text
next_month_equity_return
```

---

## Baseline model

Version 0.1 uses **Linear Regression** as a transparent baseline.

Why start simple?

1. It creates a benchmark for later models.
2. Coefficients are easy to inspect.
3. It makes it easier to detect data leakage and preprocessing mistakes.
4. It creates a clear project-growth story.

The train/test split respects time order: earlier observations are used for training and later observations for testing.

Metrics:

- MAE
- RMSE
- R²

---

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_pipeline.py
pytest
```

---

## Portfolio story

A concise interview explanation:

> I started MacroLens as a simple, reproducible data science project using macroeconomic and market time-series data. In the first version I focused on data validation, feature engineering, exploratory analysis and a transparent Linear Regression baseline. I deliberately avoided adding complex models too early because I wanted a reliable benchmark first. My next steps are to replace the demo data with real public sources, add stronger visualisation and compare regularised and non-linear models.

---

## Important limitation

The included dataset is synthetic. Therefore, the current numerical outputs should **not** be interpreted as real economic or investment conclusions.

The repository is intended to demonstrate analytical workflow and engineering practice.

---

## Next steps

See [`ROADMAP.md`](ROADMAP.md) for the planned development path.
