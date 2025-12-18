from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RaceResult(Base):
    __tablename__ = "race_results"

    __table_args__ = (
        UniqueConstraint("year", "round", "driver", name="uix_race_driver"),
    )

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    
    circuit = Column(String, nullable=False)

    driver = Column(String, nullable=False)
    team = Column(String, nullable=False)

    position = Column(Integer)
    grid = Column(Integer)
    points = Column(Float)

class QualifyingResult(Base):
    __tablename__ = "qualifying_results"

    __table_args__ = (
        UniqueConstraint("year", "round", "driver", name="uix_quali_driver"),
    )

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    circuit = Column(String, nullable=False)

    driver = Column(String, nullable=False)
    team = Column(String, nullable=False)

    position = Column(Integer)
    q1_time = Column(Float)
    q2_time = Column(Float)
    q3_time = Column(Float)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    track = Column(String, nullable=False)

    driver = Column(String, nullable=False)
    predicted_position = Column(Float, nullable=False)

    model_version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
