import pandas as pd

from src.database.connection import get_connection


def upsert_observations(df: pd.DataFrame) -> int:
    """
    Insert or update macroeconomic observations.

    The composite primary key
    (series_id, observation_date)
    prevents duplicate observations.
    """

    sql = """
        INSERT INTO macro_observations (
            series_id,
            observation_date,
            value,
            source,
            ingested_at
        )
        VALUES (%s, %s, %s, %s, %s)

        ON CONFLICT (series_id, observation_date)

        DO UPDATE SET
            value = EXCLUDED.value,
            source = EXCLUDED.source,
            ingested_at = EXCLUDED.ingested_at;
    """

    rows = []

    for row in df.itertuples(index=False):
        rows.append(
            (
                row.series_id,
                row.date.date(),
                None if pd.isna(row.value) else float(row.value),
                row.source,
                row.ingested_at,
            )
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(sql, rows)

    return len(rows)


def get_latest_observation_date(series_id: str):
    """
    Return the newest observation date
    already stored for a series.
    """

    sql = """
        SELECT MAX(observation_date)
        FROM macro_observations
        WHERE series_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (series_id,))
            result = cursor.fetchone()

    if not result:
        return None

    return result[0]


def count_observations(series_id: str) -> int:
    """
    Count stored observations for one series.
    """

    sql = """
        SELECT COUNT(*)
        FROM macro_observations
        WHERE series_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (series_id,))
            result = cursor.fetchone()

    return result[0]