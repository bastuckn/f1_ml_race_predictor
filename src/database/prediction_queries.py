import pandas as pd
from sqlalchemy import text

from src.database.connection import get_db_session

def get_predictions_for_race(
    year: int,
    round_: int,
    model_version: str | None = None
) -> pd.DataFrame:
    session = get_db_session()

    try:
        query = """
            SELECT
                year,
                round,
                track,
                driver,
                predicted_position,
                model_version,
                created_at
            FROM predictions
            WHERE year = :year
              AND round = :round
        """

        params = {"year": year, "round": round_}

        if model_version is not None:
            query += " AND model_version = :model_version"
            params["model_version"] = model_version

        query += " ORDER BY predicted_position ASC"

        df = pd.read_sql(text(query), session.bind, params=params)
        return df

    finally:
        session.close()

def get_latest_prediction_for_race(
    year: int,
    round_: int
) -> pd.DataFrame:
    session = get_db_session()

    try:
        df = pd.read_sql(
            text("""
                SELECT *
                FROM predictions
                WHERE year = :year
                  AND round = :round
                  AND created_at = (
                      SELECT MAX(created_at)
                      FROM predictions
                      WHERE year = :year
                        AND round = :round
                  )
                ORDER BY predicted_position ASC
            """),
            session.bind,
            params={"year": year, "round": round_}
        )

        return df

    finally:
        session.close()

def get_most_recent_prediction() -> pd.DataFrame:
    session = get_db_session()

    try:
        df = pd.read_sql(
            text("""
                SELECT *
                FROM predictions
                WHERE created_at = (
                    SELECT MAX(created_at)
                    FROM predictions
                )
                ORDER BY predicted_position ASC
            """),
            session.bind
        )

        return df

    finally:
        session.close()

def get_prediction_metadata(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    return {
        "year": int(df["year"].iloc[0]),
        "round": int(df["round"].iloc[0]),
        "track": df["track"].iloc[0],
        "model_version": df["model_version"].iloc[0],
        "created_at": df["created_at"].iloc[0],
    }
