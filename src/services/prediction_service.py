import time
import logging

from src.predictions.next_race import get_next_race
from src.database.predictions import prediction_exists
from src.predictions.pre_weekend import predict_pre_weekend


CHECK_INTERVAL_HRS = 1   # every hour


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

        except Exception as e:
            logging.exception(f"Service error: {e}")

        time.sleep(int(CHECK_INTERVAL_HRS * 60 * 60))
