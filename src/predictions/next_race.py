import pandas as pd
import fastf1

def get_next_race():
    fastf1.Cache.enable_cache("data/raw/fastf1_cache")

    now = pd.Timestamp.now(tz="UTC")
    year = now.year

    schedule = fastf1.get_event_schedule(year)

    # Ensure timezone-aware datetimes
    schedule["EventDate"] = pd.to_datetime(schedule["EventDate"], utc=True)

    # Keep only real race weekends
    schedule = schedule[schedule["Session5"] == "Race"]

    # Keep only future races
    future_races = schedule[schedule["EventDate"] > now]

    # Handle end-of-season case
    if future_races.empty:
        schedule = fastf1.get_event_schedule(year + 1)
        schedule["EventDate"] = pd.to_datetime(schedule["EventDate"], utc=True)
        schedule = schedule[schedule["Session5"] == "Race"]
        future_races = schedule[schedule["EventDate"] > now]

    if future_races.empty:
        raise RuntimeError("No upcoming races found")

    next_race = future_races.sort_values("EventDate").iloc[0]

    return {
        "year": int(next_race["EventDate"].year),
        "round": int(next_race["RoundNumber"]),
        "circuit": next_race["EventName"],
        "event_date": next_race["EventDate"],
    }
