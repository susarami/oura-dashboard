#dashboard
from models import get_engine
import pandas as pd
import streamlit as st

engine = get_engine()
sleep_df = pd.read_sql("SELECT * FROM daily_sleep", engine)
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