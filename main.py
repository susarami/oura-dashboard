#main
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import DailySleep, DailyActivity, DailyReadiness
from models import Base, get_engine
from datetime import datetime

engine = get_engine()
Base.metadata.create_all(engine)

load_dotenv()
token = os.getenv("OURA_TOKEN")

import requests

def fetch_oura_data(endpoint, start_date, end_date, token):
    url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {"start_date": start_date, "end_date": end_date}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    return response.json().get("data")

sleep_records = fetch_oura_data("daily_sleep", "2025-07-01", "2026-07-01", token)
readiness_records = fetch_oura_data("daily_readiness", "2025-07-01", "2026-07-01", token)
activity_records = fetch_oura_data("daily_activity", "2025-07-01", "2026-07-01", token)

Session = sessionmaker(bind=engine)
session = Session()


for record in sleep_records:
    sleep_obj = DailySleep(
        day = datetime.strptime(record["day"], "%Y-%m-%d").date(),
        score = record["score"],
        deep_sleep = record["contributors"]["deep_sleep"],
        efficiency = record["contributors"]["efficiency"],
        latency = record["contributors"]["latency"],
        rem_sleep = record["contributors"]["rem_sleep"],
        restfulness = record["contributors"]["restfulness"],
        timing = record["contributors"]["timing"],
        total_sleep = record["contributors"]["total_sleep"],

    )
    session.merge(sleep_obj)

for record in activity_records:
    activity_obj = DailyActivity(
        day = datetime.strptime(record["day"], "%Y-%m-%d").date(),
        score = record["score"],
        steps = record["steps"],
        high_activity_time = record["high_activity_time"],
        medium_activity_time = record["medium_activity_time"],
        low_activity_time = record["low_activity_time"],
        sedentary_time = record["sedentary_time"],
        recovery_time = record["contributors"]["recovery_time"],
    )
    session.merge(activity_obj)

for record in readiness_records:
    readiness_obj = DailyReadiness(
        day = datetime.strptime(record["day"], "%Y-%m-%d").date(),
        score = record["score"],
        temperature_deviation = record["temperature_deviation"],
        recovery_index = record["contributors"]["recovery_index"],
        hrv_balance = record["contributors"]["hrv_balance"],
        sleep_regularity = record["contributors"]["sleep_regularity"],
        resting_heart_rate = record["contributors"]["resting_heart_rate"],
    )
    session.merge(readiness_obj)

session.commit()

print(session.query(DailySleep).limit(5).all())
print(session.query(DailyActivity).limit(5).all())
print(session.query(DailyReadiness).limit(5).all())