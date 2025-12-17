import pandas as pd

from src.data_ingestion.fetch_fastf1 import load_session
from src.database.queries import insert_qualifying_results


def _time_to_seconds(t):
    """Convert FastF1 time to seconds (or None)."""
    if pd.isna(t):
        return None
    return t.total_seconds()


def store_qualifying_results(year: int, round: int):
    session = load_session(year, round, "Q")
    session.load()

    quali = session.results
    circuit_name = session.event["EventName"]

    rows = []

    for _, row in quali.iterrows():
        rows.append({
            "year": year,
            "round": round,
            "circuit": circuit_name,

            "driver": row["Abbreviation"],
            "team": row["TeamName"],

            "position": int(row["Position"]) if not pd.isna(row["Position"]) else None,
            "q1_time": _time_to_seconds(row["Q1"]),
            "q2_time": _time_to_seconds(row["Q2"]),
            "q3_time": _time_to_seconds(row["Q3"]),
        })

    insert_qualifying_results(rows)
