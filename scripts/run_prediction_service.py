import argparse
import logging

from src.services.prediction_service import run_service


def main(model_path: str):

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s",
    )

    run_service(model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", type=str)
    args = parser.parse_args()

    main(args.model_path)
