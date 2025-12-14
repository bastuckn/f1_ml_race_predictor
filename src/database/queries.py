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

    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()
    