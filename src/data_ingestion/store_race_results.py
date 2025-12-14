from src.data_ingestion.fetch_fastf1 import load_session
from src.database.queries import insert_race_results

def store_race_results(year: int, round: int):
    session = load_session(year, round, "R")
    results = session.results

    circuit_name = session.event["EventName"]

    rows = []

    for _, row in results.iterrows():
        rows.append({
            "year": year,
            "round": round,
            "circuit": circuit_name,
            "driver": row["Abbreviation"],
            "team": row["TeamName"],
            "position": int(row["Position"]) if row["Position"] else None,
            "grid": int(row["GridPosition"]) if row["GridPosition"] else None,
            "points": float(row["Points"]),
        })

    insert_race_results(rows)
