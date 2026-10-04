# MacroLens Roadmap

The repository is intentionally published early and improved in small, visible steps.

## v0.1 — Baseline workflow ✅
- clean repository structure
- synthetic demo dataset
- data validation
- time-series feature engineering
- correlation analysis
- Linear Regression baseline
- MAE / RMSE / R²
- basic tests

## v0.2 — Real public data
- replace synthetic data with documented public datasets
- create a source dictionary
- handle missing values and frequency alignment
- document data-quality decisions

## v0.3 — Exploratory visualisation
- macroeconomic trend charts
- return distributions
- correlation heatmap
- rolling volatility
- country comparison

## v0.4 — Stronger modelling
- Ridge Regression
- Lasso Regression
- Random Forest
- compare models against the linear baseline
- introduce time-series cross-validation

## v0.5 — Model interpretation
- feature importance
- coefficient stability
- error analysis
- discuss association vs prediction

## v0.6 — Portfolio polish
- notebook or report with key findings
- cleaner charts
- final README results section
- optional interactive dashboard

## Suggested GitHub commit story

1. `init: create reproducible macro data project structure`
2. `feat: add time-series feature engineering`
3. `feat: add baseline linear regression and evaluation`
4. `test: validate returns and lag features`
5. `data: replace demo dataset with public macro data`
6. `viz: add EDA and rolling trend charts`
7. `model: compare ridge and random forest baselines`
8. `docs: add findings, limitations and interview notes`

This sequence shows growth from a simple analytical project into a more complete data science workflow.
