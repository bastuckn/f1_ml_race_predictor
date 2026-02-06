from datetime import datetime
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

def get_prediction(
    year: int,
    round_: int,
    model_version: str | None = None
) -> pd.DataFrame:
    session: Session = get_db_session()

    query = session.query(Prediction).filter(
        Prediction.year == year,
        Prediction.round == round_
    )

    if model_version:
        query = query.filter(Prediction.model_version == model_version)

    rows = query.order_by(Prediction.predicted_position).all()
    session.close()

    if not rows:
        raise ValueError("No prediction found for this race")

    return pd.DataFrame([
        {
            "driver": r.driver,
            "team": r.team,
            "predicted_position": r.predicted_position,
            "model_version": r.model_version,
            "created_at": r.created_at,
            "track": r.track,
        }
        for r in rows
    ])
