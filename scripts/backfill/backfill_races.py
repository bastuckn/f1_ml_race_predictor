import argparse
import fastf1
from src.data_ingestion.store_race_results import store_race_results
from src.data_ingestion.store_qualifying_results import store_qualifying_results

fastf1.Cache.enable_cache("data/raw/fastf1_cache")


def backfill(start_year: int, end_year: int, session_type: str):
    for year in range(start_year, end_year + 1):
        schedule = fastf1.get_event_schedule(year)

        for _, event in schedule.iterrows():
            round_number = event["RoundNumber"]

            if session_type == "R":
                try:
                    print(f"Fetching race: {year} round {round_number}")
                    store_race_results(year, round_number)

                except Exception as e:
                    print(f"Failed {year} round {round_number}: {e}")
                    
            elif session_type == "Q":
                try:
                    print(f"Fetching qualifying: {year} round {round_number}")
                    store_qualifying_results(year, round_number)

                except Exception as e:
                    print(f"Failed {year} round {round_number}: {e}")

            else:
                raise ValueError(f"Specified a bad session_type: {session_type}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add data to the FastF1 cache")
    parser.add_argument("start_year", type=int, help="Season year to start data collection")
    parser.add_argument("end_year", type=int, help="Season year to end data collection")
    parser.add_argument("session_type", type=str, help="Type of session to fill, either R (for races) or Q (for qualifyings)")
    args = parser.parse_args()
    backfill(args.start_year, args.end_year, args.session_type)
