import time
import logging
import os

from src.predictions.next_race import get_next_race
from src.database.predictions import prediction_exists
from src.predictions.pre_weekend import predict_pre_weekend
from src.services.notify_telegram import notify_telegram
from scripts.show_prediction import get_latest_prediction_df


CHECK_INTERVAL_HRS = 1   # every hour
NOTIFY_TELEGRAM = True


def run_service(model_path: str):

    logging.info("Prediction service started")

    while True:
        try:
            next_race = get_next_race()

            year = next_race["year"]
            round_ = next_race["round"]

            logging.info(f"Next race detected: {year} round {round_}")

            if prediction_exists(year, round_):
                logging.info("Prediction already exists — skipping")
            else:
                logging.info("Creating new prediction")

                predict_pre_weekend(
                    year=year,
                    round_=round_,
                    model_path=model_path,
                    do_not_save=False,
                )

                logging.info("Prediction stored successfully")

                if NOTIFY_TELEGRAM:
                    df, track = get_latest_prediction_df(year, round_, os.path.basename(model_path), True, False)
                    df = df.sort_values("predicted_position").reset_index(drop=True)
                    df.insert(0, "P", range(1, len(df) + 1))
                    df["predicted_position"] = df["predicted_position"].round(2)
                    message = f"\n🏎️ Predicted race result for the {year} {track}:\n"
                    message += df[["P", "driver", "team"]].to_string(index=False)
                    model_used = df["model_version"].iloc[0]

                    notify_telegram(
                        f"New prediction for {year} round {round_} is ready! \n {message}"
                        )


        except Exception as e:
            logging.exception(f"Service error: {e}")

        time.sleep(int(CHECK_INTERVAL_HRS * 60 * 60))
