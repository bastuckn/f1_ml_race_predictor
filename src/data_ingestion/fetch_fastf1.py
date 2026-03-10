import fastf1
from fastf1 import get_session

# Enable cache
fastf1.Cache.enable_cache("data/raw/fastf1_cache")

def load_session(year: int, round: int, session_name: str):
    """
    session_name: 'FP1', 'FP2', 'FP3', 'Q', 'R'
    """
    session = get_session(year, round, session_name)
    session.load()
    return session

import pandas as pd
from datetime import datetime


def fetch_latest_race_results():
    current_year = datetime.now().year

    # Load the race schedule
    schedule = fastf1.get_event_schedule(current_year)

    # Keep only race sessions
    races = schedule[schedule["EventFormat"].notna()]

    # Filter races that already happened
    races = races[races["EventDate"] < datetime.now()]

    # Get the latest race
    latest_race = races.sort_values("RoundNumber").iloc[-1]

    print(latest_race)

    year = current_year
    round_ = latest_race["RoundNumber"]

    # Load the race session
    session = fastf1.get_session(year, round_, "R")
    session.load()

    results = session.results

    df = pd.DataFrame({
        "year": year,
        "round": round_,
        "circuit": latest_race["EventName"],
        "driver": results["Abbreviation"],
        "team": results["TeamName"],
        "grid": results["GridPosition"],
        "position": results["Position"],
        "points": results["Points"]
    })

    return df
