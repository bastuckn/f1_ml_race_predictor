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
    # 1. Team average quali per race
    team_race = (
        df
        .groupby(["team", "year", "round"], as_index=False)
        .agg(team_race_mean=("position", "mean"))
    )

    # 2. Rolling team form
    team_race["team_avg_finish"] = (
        team_race
        .sort_values(["team", "year", "round"])
        .groupby("team")["team_race_mean"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    # 3. Merge back to drivers
    df = df.merge(
        team_race[["team", "year", "round", "team_avg_finish"]],
        on=["team", "year", "round"],
        how="left"
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
    # 1. Team average quali per race
    team_quali = (
        df
        .groupby(["team", "year", "round"], as_index=False)
        .agg(team_quali_mean=("quali_position", "mean"))
    )

    # 2. Rolling team form
    team_quali["team_avg_quali_pos"] = (
        team_quali
        .sort_values(["team", "year", "round"])
        .groupby("team")["team_quali_mean"]
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    # 3. Merge back to drivers
    df = df.merge(
        team_quali[["team", "year", "round", "team_avg_quali_pos"]],
        on=["team", "year", "round"],
        how="left"
    )

    return df
