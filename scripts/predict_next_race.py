import argparse

from src.predictions.pre_weekend import predict_pre_weekend
from src.predictions.print_prediction import print_results
from src.predictions.next_race import get_next_race

def main(model_path: str, do_not_save: bool):

    next_race = get_next_race()

    df_out, df_session, future_race = predict_pre_weekend(year = next_race["year"], round_ = next_race["round"], model_path=model_path, do_not_save=do_not_save)

    print_results(df_session=df_session, year = next_race["year"], round_ = next_race["round"], future_race=future_race, df_out=df_out)
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict pre-weekend F1 race outcome for the next race")
    parser.add_argument("model_path", type=str, help="Path to the model to be used for prediction")
    parser.add_argument("--do_not_save", default=False, action=argparse.BooleanOptionalAction, help="Whether to store a prediction in the database")
    args = parser.parse_args()
    main(args.model_path, args.do_not_save)
