from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    track = Column(String, nullable=False)

    driver = Column(String, nullable=False)
    team = Column(String, nullable=False)

    position = Column(Integer)
    grid = Column(Integer)
    points = Column(Float)

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
