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
from src.data_ingestion.fetch_fastf1 import load_session, fetch_latest_race_results

def load_race_results():
    session = get_db_session()

    # --- check latest race stored in DB ---
    latest = (
        session.query(RaceResult.year, RaceResult.round)
        .order_by(RaceResult.year.desc(), RaceResult.round.desc())
        .first()
    )

    latest_year_db = latest.year if latest else None
    latest_round_db = latest.round if latest else None

    # --- fetch results from API ---

    df_latest = fetch_latest_race_results()

    if df_latest["round"].iloc[0] > latest_round_db:
        insert_into_db(df_latest)

    # --- determine newest race from API ---
    latest_api = df_latest.sort_values(["year", "round"]).iloc[-1]
    latest_year_api = latest_api["year"]
    latest_round_api = latest_api["round"]

    # --- check if new data exists ---
    if (
        latest_year_db is None
        or latest_year_api > latest_year_db
        or (latest_year_api == latest_year_db and latest_round_api > latest_round_db)
    ):
        print("New race results detected. Updating database...")

        for _, row in df_latest.iterrows():
            exists = session.query(RaceResult).filter_by(
                year=row["year"],
                round=row["round"],
                driver=row["driver"]
            ).first()

            if not exists:
                session.add(
                    RaceResult(
                        year=row["year"],
                        round=row["round"],
                        circuit=row["circuit"],
                        driver=row["driver"],
                        team=row["team"],
                        grid=row["grid"],
                        position=row["position"],
                        points=row["points"],
                    )
                )

        session.commit()

    # --- load full table ---
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

    if debug:
        print("Size of race df:", len(race_df))
        print("Size of quali df:", len(quali_df))

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

def insert_into_db(df_latest):
    """
    Insert the latest race results into the database.
    df_latest: pd.DataFrame with columns:
      'year', 'round', 'circuit', 'driver', 'team', 'grid', 'position', 'points'
    """
    # Convert DataFrame to list of dicts
    rows = df_latest.to_dict(orient="records")

    # Use your existing insertion function
    from src.database.queries import insert_race_results

    insert_race_results(rows)