import argparse

from src.predictions.pre_weekend import predict_pre_weekend
from src.predictions.print_prediction import print_results

def main(year: int, round_: int, model_path: str, do_not_save: bool):

    df_out, df_session, future_race = predict_pre_weekend(year=year, round_=round_, model_path=model_path, do_not_save=do_not_save)

    print_results(df_session=df_session, year=year, round_=round_, future_race=future_race, df_out=df_out)
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict pre-weekend F1 race outcome")
    parser.add_argument("year", type=int, help="Season year")
    parser.add_argument("round", type=int, help="Round number")
    parser.add_argument("model_path", type=str, help="Path to the model to be used for prediction")
    parser.add_argument("--do_not_save", default=False, action=argparse.BooleanOptionalAction, help="Whether to store a prediction in the database")
    args = parser.parse_args()
    main(args.year, args.round, args.model_path, args.do_not_save)
