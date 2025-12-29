import argparse
from src.data_ingestion.store_race_results import store_race_results
from src.data_ingestion.store_qualifying_results import store_qualifying_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add data for single events to the FastF1 cache and database")
    parser.add_argument("year", type=int, help="Season year for data collection")
    parser.add_argument("round", type=int, help="Round within year for data collection")
    parser.add_argument("session_type", type=str, help="Type of session to fill, either R (for races) or Q (for qualifyings)")
    args = parser.parse_args()

    if args.session_type == "R":
        store_race_results(year = args.year, round=args.round)
        print("Race results stored.")
    elif args.session_type == "Q":
        store_qualifying_results(year = args.year, round=args.round)
        print("Qualifying results stored.")
    else:
        raise ValueError(f"Specified a bad session_type: {args.session_type}")
    