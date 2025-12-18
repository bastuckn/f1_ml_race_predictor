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
