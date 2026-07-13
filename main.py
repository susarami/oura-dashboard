from dotenv import load_dotenv
import os

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

print(len(sleep_records), len(readiness_records), len(activity_records))