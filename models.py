#models
from sqlalchemy import create_engine, Column, Integer, Date
from sqlalchemy.orm import declarative_base
import os

Base = declarative_base()

class DailySleep(Base):
    __tablename__ = 'daily_sleep'

    day = Column(Date, primary_key=True)
    score = Column(Integer)
    deep_sleep = Column(Integer)
    efficiency = Column(Integer)
    latency = Column(Integer)
    rem_sleep = Column(Integer)
    restfulness = Column(Integer)
    timing = Column(Integer)
    total_sleep = Column(Integer)

def get_engine():
    os.makedirs("data", exist_ok=True)
    engine = create_engine('sqlite:///data/oura.db')
    return engine

engine = get_engine()
