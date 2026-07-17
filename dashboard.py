#dashboard
from datetime import timedelta
from models import get_engine
import pandas as pd
import streamlit as st

engine = get_engine()
sleep_df = pd.read_sql("SELECT * FROM daily_sleep", engine)
sleep_df["day"] = pd.to_datetime(sleep_df["day"])

def is_previous_day_workday(day):
    previous_day = day - timedelta(days=1)
    return previous_day.weekday() in {1, 5, 6}

sleep_df["worked_previous_day"] = sleep_df["day"].apply(is_previous_day_workday)

activity_df = pd.read_sql("SELECT * FROM daily_activity", engine)
readiness_df = pd.read_sql("SELECT * FROM daily_readiness", engine)

st.title("Oura Dashboard")
st.header("Sleep - Score, Timing, Latency")
st.line_chart(sleep_df.set_index("day")[["score", "timing", "latency"]])

st.header("Sleep - Efficiency, Total Sleep")
st.line_chart(sleep_df.set_index("day")[["efficiency", "total_sleep"]])

st.header("Sleep - REM, Restfulness")
st.line_chart(sleep_df.set_index("day")[["rem_sleep", "restfulness"]])

st.header("Activity")
st.line_chart(activity_df.set_index("day")["score"])

st.header("Readiness")
st.line_chart(readiness_df.set_index("day")["score"])

print(sleep_df.head())
print(sleep_df[["day", "worked_previous_day"]].head(10))