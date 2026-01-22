import os
import argparse
import pandas as pd
import joblib
import fastf1

from src.feature_engineering.build_features import build_feature_table
from src.database.predictions import store_predictions

def predict_pre_weekend(year: int, round_: int, model_path: str, do_not_save: bool):

    # 1. Load feature table (pre-weekend features only)
    df_features = build_feature_table()

    future_race = not race_exists(year, round_, df_features)

    # see if race is past or future:
    if future_race:
        if ((year == 2026) and (round_ == 1)):
            # hard-coded lineup for 2026, round 1, to bridge the gap before the first race
            # alternatively, read in the free practice results to also get some data
            df_features = pd.read_csv("data/2026_1.csv")
        else:
            df_last = get_latest_known_race(df_features)
            df_last = adapt_for_future_race(df_last, year, round_)
            df_features = pd.concat([df_features,df_last])
            # df_features[df_features["year"] == 2026].to_csv(path_or_buf="data/2026_1.csv")

    # Select session we want to predict
    df_session = df_features[
        (df_features["year"] == year) &
        (df_features["round"] == round_)
    ].copy()

    # 2. Load trained pre-weekend model
    bundle = joblib.load(model_path)
    model = bundle["model"]
    feature_cols = bundle["features"]  # pre-weekend features used in training

    # 3. Select feature columns for prediction
    missing_cols = [c for c in feature_cols if c not in df_session.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in feature table: {missing_cols}")
    
    x = df_session[feature_cols]

    pd.set_option('display.max_columns', None)

    # 4. Make predictions
    df_session["position_pred"] = model.predict(x)

    # 5. Output predictions
    df_session = add_driver_columns(df_session)
    df_session = add_team_columns(df_session)
   
    df_out = (
        df_session[["driver_id", "team_id", "position_pred"]]
        .sort_values("position_pred")
        .reset_index(drop=True)
    )

    if not do_not_save:
        # Store predictions BEFORE formatting
        model_version = os.path.basename(model_path)
        circuit = get_circuit(df_session)

        store_predictions(
            year=year,
            round_=round_,
            track=circuit,
            model_version=model_version,
            df_predictions=df_out
        )

    return df_out, df_session, future_race

def get_circuit(df_session):
    circuit_cols = [c for c in df_session.columns if c.startswith("circuit_")]

    if not circuit_cols:
        raise ValueError("No circuit_* columns found in feature table")

    # Ensure numeric (important!)
    circuit_df = df_session[circuit_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    circuit = (
        circuit_df
        .idxmax(axis=1)
        .str.replace("circuit_", "")
        .iloc[0]
    )

    return circuit

def add_driver_columns(df_session):
    driver_cols = [c for c in df_session.columns if c.startswith("driver_") 
               and df_session[c].nunique() == 2]

    df_session["driver_id"] = df_session[driver_cols].idxmax(axis=1).str.replace("driver_", "")

    return df_session

def add_team_columns(df_session):
    team_cols = [c for c in df_session.columns if c.startswith("team_") and df_session[c].nunique() == 2]

    df_session["team_id"] = df_session[team_cols].idxmax(axis=1).str.replace("team_", "")

    return df_session

def race_exists(year, round_, df_features):
    return ((df_features["year"] == year) & (df_features["round"] == round_)).any()

def get_latest_known_race(df_features):
    return (
        df_features
        .sort_values(["year", "round"])
        .groupby(["year", "round"])
        .tail(20)  # one row per driver
        .iloc[-20:]
    )

def adapt_for_future_race(df_last, target_year, target_round):
    df_future = df_last.copy()

    df_future["year"] = target_year
    df_future["round"] = target_round

    # Reset circuit one-hot
    circuit_cols = [c for c in df_future.columns if c.startswith("circuit_")]
    df_future[circuit_cols] = 0

    target_circuit = determine_circuit(target_year, target_round)

    # Activate target circuit
    df_future[f"circuit_{target_circuit}"] = 1

    return df_future

def determine_circuit(year, round_):
    fastf1.Cache.enable_cache("data/raw/fastf1_cache")
    schedule = fastf1.get_event(year, round_)
    return schedule["EventName"]
