import pandas as pd
from src.database.connection import get_db_session
from src.database.models import RaceResult

def load_race_results():
    session = get_db_session()
    rows = session.query(RaceResult).all()
    session.close()

    data = [{
        "year": r.year,
        "round": r.round,
        "circuit": r.circuit,
        "driver": r.driver,
        "team": r.team,
        "grid": r.grid,
        "position": r.position,
        "points": r.points,
    } for r in rows]

    return pd.DataFrame(data)
