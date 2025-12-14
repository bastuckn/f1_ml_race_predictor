from src.data_ingestion.store_race_results import store_race_results

if __name__ == "__main__":
    store_race_results(year=2024, round=1)
    print("Race results stored.")
