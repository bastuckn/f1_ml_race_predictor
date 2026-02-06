def format_prediction_table(df, year, round_, track):
    df = df.sort_values("predicted_position").reset_index(drop=True)
    df.insert(0, "P", range(1, len(df) + 1))
    df["predicted_position"] = df["predicted_position"].round(2)

    print(f"\n🏎️ Predicted race result for the {year} {track}:\n")
    print(df[["P", "driver", "team", "predicted_position"]].to_string(index=False))
