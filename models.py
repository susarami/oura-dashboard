#models
from sqlalchemy import create_engine, Column, Integer, Date, Float
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

class DailyActivity(Base):
    __tablename__ = 'daily_activity'
    day = Column(Date, primary_key=True)
    score = Column(Integer)
    steps = Column(Integer)
    high_activity_time = Column(Integer)
    medium_activity_time = Column(Integer)
    low_activity_time = Column(Integer)
    sedentary_time = Column(Integer)

class DailyReadiness(Base):
    __tablename__ = 'daily_readiness'
    day = Column(Date, primary_key=True)
    score = Column(Integer)
    temperature_deviation = Column(Float)
    recovery_index = Column(Integer)
    hrv_balance = Column(Integer)
    sleep_regularity = Column(Integer)
    resting_heart_rate = Column(Integer)


def get_engine():
    os.makedirs("data", exist_ok=True)
    engine = create_engine('sqlite:///data/oura.db')
    return engine

engine = get_engine()
