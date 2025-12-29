import argparse
import pandas as pd
import joblib
import fastf1

from src.feature_engineering.build_features import build_feature_table

def main(year: int, round_: int, model_path: str):

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
    df_out.insert(0, "P", range(1, len(df_out) + 1))
    df_out["position_pred"] = df_out["position_pred"].round(2)

    print_results(df_session, year, round_, future_race, df_out)

    return 0

def print_results(df_session, year, round_, future_race, df_out):
    df_actual = get_actual_results(df_session, year, round_)

    if df_actual is not None and not future_race:
        df_out = df_out.merge(df_actual, on="driver_id", how="left")

        # Prediction error
        df_out["Δ"] = df_out["Actual Pos"] - df_out["P"]
    
    df_out = df_out.rename(columns={
        "driver_id": "Driver",
        "team_id": "Team",
        "position_pred": "Predicted Pos"
    })

    year = get_year(df_session)
    circuit = get_circuit(df_session)

    print(f"\n🏎️ Predicted race result for the {year} {circuit}:\n")
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

def get_actual_results(df_all, year, round_):
    df_actual = df_all[
        (df_all["year"] == year) &
        (df_all["round"] == round_)
    ][["driver_id", "position"]]

    if df_actual.empty:
        return None

    return df_actual.rename(columns={"position": "Actual Pos"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict pre-weekend F1 race outcome")
    parser.add_argument("year", type=int, help="Season year")
    parser.add_argument("round", type=int, help="Round number")
    parser.add_argument("model_path", type=str, help="Path to the model to be used for prediction")
    args = parser.parse_args()
    main(args.year, args.round, args.model_path)
