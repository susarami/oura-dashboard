#dashboard
from datetime import timedelta
from models import get_engine
import pandas as pd
import streamlit as st
from scipy import stats

engine = get_engine()
sleep_df = pd.read_sql("SELECT * FROM daily_sleep", engine)
sleep_df["day"] = pd.to_datetime(sleep_df["day"])

def is_previous_day_workday(day):
    previous_day = day - timedelta(days=1)
    return previous_day.weekday() in {1, 5, 6}

sleep_df["worked_previous_day"] = sleep_df["day"].apply(is_previous_day_workday)

sleep_worked = sleep_df[sleep_df["worked_previous_day"] == True]["efficiency"]
sleep_rested = sleep_df[sleep_df["worked_previous_day"] == False]["efficiency"]

sleep_t_stat, sleep_p_value = stats.ttest_ind(sleep_worked, sleep_rested)

print("Efficiency")
print(sleep_df.groupby("worked_previous_day")["efficiency"].mean())
print(sleep_df.groupby("worked_previous_day")["efficiency"].count())
print(sleep_t_stat)
print(sleep_p_value)

activity_df = pd.read_sql("SELECT * FROM daily_activity", engine)
activity_df["day"] = pd.to_datetime(activity_df["day"])
activity_df["worked_previous_day"] = activity_df["day"].apply(is_previous_day_workday)
activity_worked = activity_df[activity_df["worked_previous_day"] == True]["recovery_time"]
activity_rested = activity_df[activity_df["worked_previous_day"] == False]["recovery_time"]
activity_t_stat, activity_p_value = stats.ttest_ind(activity_worked, activity_rested, nan_policy="omit")

print("Recovery Time")
print(activity_df.groupby("worked_previous_day")["recovery_time"].mean())
print(activity_df.groupby("worked_previous_day")["recovery_time"].count())
print(activity_t_stat)
print(activity_p_value)

readiness_df = pd.read_sql("SELECT * FROM daily_readiness", engine)
readiness_df["day"] = pd.to_datetime(readiness_df["day"])
readiness_df["worked_previous_day"] = readiness_df["day"].apply(is_previous_day_workday)
readiness_worked = readiness_df[readiness_df["worked_previous_day"] == True]["resting_heart_rate"]
readiness_rested = readiness_df[readiness_df["worked_previous_day"] == False]["resting_heart_rate"]
readiness_t_stat, readiness_p_value = stats.ttest_ind(readiness_worked, readiness_rested, nan_policy="omit")

print("Readiness score")
print(readiness_df.groupby("worked_previous_day")["resting_heart_rate"].mean())
print(readiness_df.groupby("worked_previous_day")["resting_heart_rate"].count())
print(readiness_t_stat)
print(readiness_p_value)

st.header("Sleep")
sleep_means = sleep_df.groupby("worked_previous_day")["efficiency"].mean()
rested_score = sleep_means.loc[False]
worked_score = sleep_means.loc[True]

col1, col2 = st.columns(2)
col1.metric("Sleep Efficiency - After Day Off", f"{rested_score:.1f}")
col2.metric("Sleep Efficiency - After Work Day", f"{worked_score:.1f}", delta = f"{worked_score - rested_score:.1f}")
st.bar_chart(sleep_means)
st.caption(f"t-test: t = {sleep_t_stat:.2f}, p = {sleep_p_value:.6f}")

st.header("Activity")
activity_means = activity_df.groupby("worked_previous_day")["recovery_time"].mean()
rested_score = activity_means.loc[False]
worked_score = activity_means.loc[True]

col3, col4 = st.columns(2)
col3.metric("Recovery Time - After Day Off", f"{rested_score:.1f}")
col4.metric("Recovery - After Work Day", f"{worked_score:.1f}", delta = f"{worked_score - rested_score:.1f}")
st.bar_chart(activity_means)
st.caption(f"t-test: t = {activity_t_stat:.2f}, p = {activity_p_value:.6f}")

st.header("Readiness")
readiness_means = readiness_df.groupby("worked_previous_day")["resting_heart_rate"].mean()
rested_score = readiness_means.loc[False]
worked_score = readiness_means.loc[True]

col5, col6 = st.columns(2)
col5.metric("Resting Heart Rate - After Day Off", f"{rested_score:.1f}")
col6.metric("Resting Heart Rate - After Work Day", f"{worked_score:.1f}", delta = f"{worked_score - rested_score:.1f}")
st.bar_chart(readiness_means)
st.caption(f"t-test: t = {readiness_t_stat:.2f}, p = {readiness_p_value:.6f}")