import pandas as pd

from src.database.connection import get_db_session
from src.database.models import RaceResult
from src.feature_engineering.aggregations import add_driver_form, add_team_form
from src.feature_engineering.encoders import encode_categoricals

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

def build_feature_table(debug=False):
    df = load_race_results()

    df = add_driver_form(df)
    df = add_team_form(df)

    df = encode_categoricals(df)

    if debug:
        print(df.isnull().sum())
        print(df.describe())

    return df

def save_features(df, path="data/processed/features.csv"):
    df.to_csv(path, index=False)
