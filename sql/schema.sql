CREATE TABLE IF NOT EXISTS macro_observations (
    series_id VARCHAR(50) NOT NULL,
    observation_date DATE NOT NULL,
    value DOUBLE PRECISION,
    source VARCHAR(50) NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (series_id, observation_date)
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id BIGSERIAL PRIMARY KEY,
    series_id VARCHAR(50) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL,
    rows_processed INTEGER DEFAULT 0
);   ---observability

