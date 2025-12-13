from src.data_ingestion.fetch_fastf1 import load_session

if __name__ == "__main__":
    session = load_session(2024, 1, "R")  # Bahrain GP Race
    results = session.results

    print(results[["DriverNumber", "Abbreviation", "Position", "Points"]])
