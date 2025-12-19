import pandas as pd

from src.database.connection import get_db_session
from src.database.models import RaceResult, QualifyingResult

from src.feature_engineering.aggregations import (
    add_driver_form,
    add_team_form,
    add_driver_quali_form,
    add_team_quali_form,
)

from src.feature_engineering.encoders import encode_categoricals

def load_race_results():
    session = get_db_session()
    rows = session.query(RaceResult).all()
    session.close()

    return pd.DataFrame([{
        "year": r.year,
        "round": r.round,
        "circuit": r.circuit,
        "driver": r.driver,
        "team": r.team,
        "grid": r.grid,
        "position": r.position,
        "points": r.points,
    } for r in rows])


def load_qualifying_results():
    session = get_db_session()
    rows = session.query(QualifyingResult).all()
    session.close()

    return pd.DataFrame([{
        "year": q.year,
        "round": q.round,
        "circuit": q.circuit,
        "driver": q.driver,
        "team": q.team,
        "quali_position": q.position,
        "q1_time": q.q1_time,
        "q2_time": q.q2_time,
        "q3_time": q.q3_time,
    } for q in rows])


def build_feature_table(debug: bool = False):
    # Load base race data (always required)
    race_df = load_race_results()

    # Merge qualifying data into same rows
    quali_df = load_qualifying_results()

    df = race_df.merge(
        quali_df,
        on=["year", "round", "driver", "team", "circuit"],
        how="left"
    )

    df = additional_features(df)

    # --- Sanity checks
    if debug:
        print("Null counts:")
        print(df.isnull().sum().sort_values(ascending=False).head(15))

        print("\nFeature describe:")
        print(df.describe())

        print("\nQualifying coverage:")
        print(df["quali_position"].isna().mean())

    return df

def additional_features(df):
    # --- Race-based rolling features (leakage-safe)
    df = add_driver_form(df)
    df = add_team_form(df)

    # --- Qualifying-based features
    df = add_driver_quali_form(df)
    df = add_team_quali_form(df)

    # --- Encode categoricals
    df = encode_categoricals(df)

    return df

def save_features(df, path="data/processed/features.csv"):
    df.to_csv(path, index=False)
