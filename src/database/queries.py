from sqlalchemy.exc import IntegrityError
from src.database.models import RaceResult
from src.database.connection import get_db_session

def insert_race_results(results):
    """
    results: list[dict]
    """
    session = get_db_session()

    try:
        for row in results:
            record = RaceResult(**row)
            session.add(record)

        session.commit()

    except IntegrityError:
        session.rollback()

        # Delete existing rows for this race and retry
        year = results[0]["year"]
        round_ = results[0]["round"]

        session.query(RaceResult).filter(
            RaceResult.year == year,
            RaceResult.round == round_
        ).delete()

        session.commit()

        # Retry insert
        for row in results:
            record = RaceResult(**row)
            session.add(record)

        session.commit()

    finally:
        session.close()
