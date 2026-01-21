from datetime import datetime
from sqlalchemy.exc import IntegrityError

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
