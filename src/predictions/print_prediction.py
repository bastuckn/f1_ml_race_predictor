import pandas as pd

def print_results(df_session, year, round_, future_race, df_out):

    # Pretty output
    df_out.insert(0, "P", range(1, len(df_out) + 1))
    df_out["position_pred"] = df_out["position_pred"].round(2)

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

def get_actual_results(df_all, year, round_):
    df_actual = df_all[
        (df_all["year"] == year) &
        (df_all["round"] == round_)
    ][["driver_id", "position"]]

    if df_actual.empty:
        return None

    return df_actual.rename(columns={"position": "Actual Pos"})