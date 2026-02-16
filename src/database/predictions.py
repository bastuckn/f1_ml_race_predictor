from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
import pandas as pd

from src.database.connection import get_db_session
from src.database.models import Prediction  # if ORM exists

def store_predictions(
    year: int,
    round_: int,
    track: str,
    model_version: str,
    df_predictions
):
    """
    df_predictions must contain:
    - driver_id
    - position_pred
    """
    session = get_db_session()

    try:
        # Remove existing predictions for this race + model
        session.query(Prediction).filter(
            Prediction.year == year,
            Prediction.round == round_,
            Prediction.model_version == model_version
        ).delete()

        session.commit()

        # Insert new predictions
        for _, row in df_predictions.iterrows():
            pred = Prediction(
                year=year,
                round=round_,
                track=track,
                driver=row["driver_id"],
                team=row['team_id'],
                predicted_position=float(row["position_pred"]),
                model_version=model_version,
                created_at=datetime.now()
            )
            session.add(pred)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

from sqlalchemy import func

def get_prediction(year: int, round_: int, model_version: str | None = None):
    session = get_db_session()

    base_query = session.query(Prediction).filter(
        Prediction.year == year,
        Prediction.round == round_
    )

    if model_version:
        rows = (
            base_query
            .filter(Prediction.model_version == model_version)
            .order_by(Prediction.predicted_position)
            .all()
        )
    else:
        # ✅ Get model_version of most recent prediction run
        latest_model = (
            base_query
            .order_by(Prediction.created_at.desc())
            .limit(1)
            .with_entities(Prediction.model_version)
            .scalar()
        )

        if latest_model is None:
            session.close()
            raise ValueError("No predictions found for this race")

        rows = (
            base_query
            .filter(Prediction.model_version == latest_model)
            .order_by(Prediction.predicted_position)
            .all()
        )

    session.close()
    return rows

# ensures that we do not update the prediction throughout the weekend:
def prediction_exists(year: int, round_: int) -> bool:
    session = get_db_session()

    try:
        exists = (
            session.query(Prediction)
            .filter(
                Prediction.year == year,
                Prediction.round == round_,
            )
            .first()
            is not None
        )
        return exists

    finally:
        session.close()