import fastf1
from fastf1 import get_session

# Enable cache
fastf1.Cache.enable_cache("data/raw/fastf1_cache")

def load_session(year: int, round: int, session_name: str):
    """
    session_name: 'FP1', 'FP2', 'FP3', 'Q', 'R'
    """
    session = get_session(year, round, session_name)
    session.load()
    return session
