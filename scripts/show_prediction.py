import argparse

from src.database.predictions import get_prediction
from src.predictions.next_race import get_next_race
from src.predictions.display import format_prediction_table

def main(year, round_, model_version, next_race):
    if next_race:
        race = get_next_race()
        year = race["year"]
        round_ = race["round"]
        track = race["circuit"]
    else:
        track = None

    df = get_prediction(year, round_, model_version)

    if track is None:
        track = df["track"].iloc[0]

    format_prediction_table(df, year, round_, track)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show stored F1 predictions")
    parser.add_argument("--year", type=int)
    parser.add_argument("--round", type=int)
    parser.add_argument("--model", dest="model_version", type=str)
    parser.add_argument("--next", action="store_true", help="Show next race prediction")

    args = parser.parse_args()

    if not args.next and (args.year is None or args.round is None):
        parser.error("Either --next or both --year and --round must be specified")

    main(args.year, args.round, args.model_version, args.next)
