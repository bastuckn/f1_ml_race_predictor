import argparse
import pandas as pd
import joblib
from src.feature_engineering.build_features import build_feature_table

MODEL_NAME = "race_position_model_2025-12-18.pkl"

def main(year: int, round_: int):
    # --------------------------------------------------
    # 1. Load feature table (pre-weekend features only)
    # --------------------------------------------------
    df_features = build_feature_table()

    # Keep identifiers for merging/output
    identifiers = ["driver_id", "team_id", "circuit", "year", "round"]

    # Select session we want to predict
    df_session = df_features[
        (df_features["year"] == year) &
        (df_features["round"] == round_)
    ].copy()

    if df_session.empty:
        raise ValueError(f"No features found for Year={year}, Round={round_}")

    # --------------------------------------------------
    # 2. Load trained pre-weekend model
    # --------------------------------------------------
    bundle = joblib.load("models/" + MODEL_NAME)
    model = bundle["model"]
    feature_cols = bundle["features"]  # pre-weekend features used in training

    # --------------------------------------------------
    # 3. Select feature columns for prediction
    # --------------------------------------------------
    missing_cols = [c for c in feature_cols if c not in df_session.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in feature table: {missing_cols}")

    X = df_session[feature_cols]

    # --------------------------------------------------
    # 4. Make predictions
    # --------------------------------------------------
    df_session["position_pred"] = model.predict(X)

    # --------------------------------------------------
    # 5. Output predictions
    # --------------------------------------------------
    df_session = add_driver_columns(df_session)
    df_session = add_team_columns(df_session)
   
    df_out = df_session[["driver_id", "team_id"] + ["position_pred"]].sort_values("position_pred")
    print("I have predicted the following race result for the " + str(get_year(df_session)) + " " + str(get_circuit(df_session)) + ": \n")
    print(df_out.to_string(index=False))

def get_year(df_session):
    return df_session["year"].iloc[0]

def get_circuit(df_session):
     # Identify circuit one-hot columns
    circuit_cols = [c for c in df_session.columns if c.startswith("circuit_")]

    # Extract the circuit name
    df_session["circuit_name"] = df_session[circuit_cols].idxmax(axis=1).str.replace("circuit_", "")

    # Since all rows are for the same session, take the first one
    circuit = df_session["circuit_name"].iloc[0]
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict pre-weekend F1 race outcome")
    parser.add_argument("year", type=int, help="Season year")
    parser.add_argument("round", type=int, help="Round number")
    args = parser.parse_args()
    main(args.year, args.round)
