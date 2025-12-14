from src.database.connection import get_db_session
from src.database.models import RaceResult

session = get_db_session()

rows = session.query(RaceResult).limit(5).all()

for r in rows:
    print(r.year, r.round, r.circuit, r.driver, r.position)

session.close()
