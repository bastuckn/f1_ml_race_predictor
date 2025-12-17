import fastf1
from src.data_ingestion.store_race_results import store_race_results

fastf1.Cache.enable_cache("data/raw/fastf1_cache")

START_YEAR = 2020
END_YEAR = 2025


def backfill():
    for year in range(START_YEAR, END_YEAR + 1):
        schedule = fastf1.get_event_schedule(year)

        for _, event in schedule.iterrows():
            round_number = event["RoundNumber"]

            try:
                print(f"Fetching race: {year} round {round_number}")
                store_race_results(year, round_number)

            except Exception as e:
                print(f"Failed {year} round {round_number}: {e}")


if __name__ == "__main__":
    backfill()
