def add_driver_form(df, window=5):
    df = df.sort_values(["driver", "year", "round"])

    df["driver_avg_finish"] = (
        df.groupby("driver")["position"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df

def add_team_form(df, window=5):
    df = df.sort_values(["team", "year", "round"])

    df["team_avg_finish"] = (
        df.groupby("team")["position"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df

def add_quali_gap(df):
    df["best_quali_time"] = df[["q1_time", "q2_time", "q3_time"]].min(axis=1)

    pole_times = (
        df.groupby(["year", "round"])["best_quali_time"]
        .min()
        .rename("pole_time")
    )

    df = df.merge(
        pole_times,
        on=["year", "round"],
        how="left"
    )

    df["quali_gap_to_pole"] = df["best_quali_time"] - df["pole_time"]

    return df.drop(columns=["best_quali_time", "pole_time"])

def add_driver_quali_form(df, window=5):
    df = df.sort_values(["driver", "year", "round"])

    df["driver_avg_quali_pos"] = (
        df.groupby("driver")["quali_position"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df

def add_team_quali_form(df, window=5):
    df = df.sort_values(["team", "year", "round"])

    df["team_avg_quali_pos"] = (
        df.groupby("team")["quali_position"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    return df
