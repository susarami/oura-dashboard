#dashboard
from datetime import timedelta
from models import get_engine
import pandas as pd
import streamlit as st
from scipy import stats
import plotly.express as px

engine = get_engine()
sleep_df = pd.read_sql("SELECT * FROM daily_sleep", engine)
sleep_df = sleep_df.rename(columns={"score": "sleep_score"})
sleep_df["day"] = pd.to_datetime(sleep_df["day"])

work_shifts_df = pd.read_sql("SELECT * FROM work_shifts", engine)
work_shifts_df["day"] = pd.to_datetime(work_shifts_df["day"])

worked_days = set(work_shifts_df["day"].dt.date)
print(len(worked_days))

print(work_shifts_df.head())

def is_previous_day_workday(day):
    previous_day = day - timedelta(days=1)
    return previous_day.date() in worked_days

def is_workday(day):
    return day.date() in worked_days

def was_sick(day):
    range1 = day >= pd.Timestamp("2025-08-11") and day <= pd.Timestamp("2025-08-23")
    range2 = day >= pd.Timestamp("2025-10-19") and day <= pd.Timestamp("2025-10-25")
    range3 = day >= pd.Timestamp("2025-11-02") and day <= pd.Timestamp("2025-11-04")
    return range1 or range2 or range3

def consecutive_workdays_before(day):
    one_day_back = day - timedelta(days=1)
    two_day_back = day - timedelta(days=2)
    return is_workday(one_day_back) + is_workday(two_day_back)

sleep_df["worked_previous_day"] = sleep_df["day"].apply(is_previous_day_workday)
sleep_df["score_7day_avg"] = sleep_df["sleep_score"].rolling(window = 7).mean()

st.header("Sleep Score Rolling 7 Day Average")
st.line_chart(sleep_df.set_index("day")[["sleep_score", "score_7day_avg"]])

sleep_worked = sleep_df[sleep_df["worked_previous_day"] == True]["efficiency"]
sleep_rested = sleep_df[sleep_df["worked_previous_day"] == False]["efficiency"]

sleep_t_stat, sleep_p_value = stats.ttest_ind(sleep_worked, sleep_rested)

#print("Efficiency")
#print(sleep_df.groupby("worked_previous_day")["efficiency"].mean())
#print(sleep_df.groupby("worked_previous_day")["efficiency"].count())
#print(sleep_t_stat)
#print(sleep_p_value)

activity_df = pd.read_sql("SELECT * FROM daily_activity", engine)
activity_df = activity_df.rename(columns={"score": "activity_score"})
activity_df["day"] = pd.to_datetime(activity_df["day"])
activity_df["worked_previous_day"] = activity_df["day"].apply(is_previous_day_workday)
activity_df["was_sick"] = activity_df["day"].apply(was_sick)
activity_df.loc[activity_df["was_sick"], "activity_score"] = pd.NA
activity_df["score_7day_avg"] = activity_df["activity_score"].rolling(window = 7).mean()
st.header("Activity Score Rolling 7 Day Average")
st.line_chart(activity_df.set_index("day")[["activity_score", "score_7day_avg"]])


activity_worked = activity_df[activity_df["worked_previous_day"] == True]["recovery_time"]
activity_rested = activity_df[activity_df["worked_previous_day"] == False]["recovery_time"]
activity_t_stat, activity_p_value = stats.ttest_ind(activity_worked, activity_rested, nan_policy="omit")

#print("Recovery Time")
#print(activity_df.groupby("worked_previous_day")["recovery_time"].mean())
#print(activity_df.groupby("worked_previous_day")["recovery_time"].count())
#print(activity_t_stat)
#print(activity_p_value)

readiness_df = pd.read_sql("SELECT * FROM daily_readiness", engine)
readiness_df = readiness_df.rename(columns={"score": "readiness_score"})
readiness_df["day"] = pd.to_datetime(readiness_df["day"])
readiness_df["worked_previous_day"] = readiness_df["day"].apply(is_previous_day_workday)

readiness_df["score_7day_avg"] = readiness_df["readiness_score"].rolling(window = 7).mean()
st.header("Readiness Score Rolling 7 Day Average")
st.line_chart(readiness_df.set_index("day")[["readiness_score", "score_7day_avg"]])

readiness_worked = readiness_df[readiness_df["worked_previous_day"] == True]["resting_heart_rate"]
readiness_rested = readiness_df[readiness_df["worked_previous_day"] == False]["resting_heart_rate"]
readiness_t_stat, readiness_p_value = stats.ttest_ind(readiness_worked, readiness_rested, nan_policy="omit")

#print("Readiness score")
#print(readiness_df.groupby("worked_previous_day")["resting_heart_rate"].mean())
#print(readiness_df.groupby("worked_previous_day")["resting_heart_rate"].count())
#print(readiness_t_stat)
#print(readiness_p_value)

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
col4.metric("Recovery Time - After Work Day", f"{worked_score:.1f}", delta = f"{worked_score - rested_score:.1f}")
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


combined_df = sleep_df.merge(readiness_df, on = "day")
combined_df = combined_df.merge(activity_df, on = "day")
combined_df["worked_previous_day"] = combined_df["day"].apply(is_previous_day_workday)
combined_df = combined_df.drop(columns = ["worked_previous_day_x", "worked_previous_day_y"])
combined_df["is_workday"] = combined_df["day"].apply(is_workday)
combined_df["consecutive_workdays_before"] = combined_df["day"].apply(consecutive_workdays_before)
print(combined_df.columns)

correlation_matrix = combined_df.corr(numeric_only = True)
print(correlation_matrix)

focus_columns = ["is_workday", "steps", "low_activity_time", "sedentary_time"]
focus_corr = combined_df[focus_columns].corr(numeric_only = True)

fig = px.imshow(focus_corr, text_auto = True, color_continuous_scale = "RdBu", zmin = -1, zmax = 1)
st.plotly_chart(fig)

#print(combined_df.groupby("consecutive_workdays_before")["sleep_score"].mean())
#print(combined_df.groupby("consecutive_workdays_before")["sleep_score"].count())
#
#group0 = combined_df[combined_df["consecutive_workdays_before"] == 0]["sleep_score"]
#group1 = combined_df[combined_df["consecutive_workdays_before"] == 1]["sleep_score"]
#group2 = combined_df[combined_df["consecutive_workdays_before"] == 2]["sleep_score"]
#
#combined_f_stat, combined_p_value = stats.f_oneway(group0, group1, group2)
#print(combined_f_stat)
#print(combined_p_value)

#print(combined_df.groupby("consecutive_workdays_before")["resting_heart_rate"].mean())
#print(combined_df.groupby("consecutive_workdays_before")["resting_heart_rate"].count())
#
#group0 = combined_df[combined_df["consecutive_workdays_before"] == 0]["resting_heart_rate"]
#group1 = combined_df[combined_df["consecutive_workdays_before"] == 1]["resting_heart_rate"]
#group2 = combined_df[combined_df["consecutive_workdays_before"] == 2]["resting_heart_rate"]
#
#combined_f_stat, combined_p_value = stats.f_oneway(group0, group1, group2, nan_policy = "omit")
#print(combined_f_stat)
#print(combined_p_value)

print(combined_df.groupby("consecutive_workdays_before")["recovery_time"].mean())
print(combined_df.groupby("consecutive_workdays_before")["recovery_time"].count())

group0 = combined_df[combined_df["consecutive_workdays_before"] == 0]["recovery_time"]
group1 = combined_df[combined_df["consecutive_workdays_before"] == 1]["recovery_time"]
group2 = combined_df[combined_df["consecutive_workdays_before"] == 2]["recovery_time"]

combined_f_stat, combined_p_value = stats.f_oneway(group0, group1, group2, nan_policy = "omit")
print(combined_f_stat)
print(combined_p_value)


print(activity_df["activity_score"].isna().sum())
print(activity_df[activity_df["activity_score"] == 0])

mondays = combined_df[combined_df["day"].dt.weekday == 0]
print(mondays[["day", "consecutive_workdays_before"]].head())

st.header("Consecutive Workdays Compounding Effect on Recovery Time")
compounded_means = combined_df.groupby("consecutive_workdays_before")["recovery_time"].mean()
col1, col2, col3 = st.columns(3)
col1.metric("0 Consecutive Work Days", f"{compounded_means[0]:.1f}")
col2.metric("1 Consecutive Work Days", f"{compounded_means[1]:.1f}", delta = f"{compounded_means.loc[1] - compounded_means[0]:.1f}")
col2.metric("2 Consecutive Work Days", f"{compounded_means[2]:.1f}", delta = f"{compounded_means.loc[2] - compounded_means[1]:.1f}")
st.bar_chart(compounded_means)
st.caption(f"One-way ANOVA: t = {combined_f_stat:.2f}, p = {combined_p_value:.6f}")

sleep_df.to_csv("sleep_df.csv", index = False)
activity_df.to_csv("activity_df.csv", index = False)
readiness_df.to_csv("readiness_df.csv", index = False)

st.subheader("Sleep Efficiency: Rolling 7-Day Trend")

query = """
SELECT
    day,
    efficiency,
    AVG(efficiency) OVER (
        ORDER BY day
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_efficiency
FROM daily_sleep
ORDER BY day;
"""
df = pd.read_sql(query, engine, parse_dates = ["day"])
df = df.set_index("day")

st.line_chart(df[["efficiency", "rolling_7day_efficiency"]])

st.subheader("Readiness: Day-over-day Change")

readiness_query = """
SELECT
    day,
    score AS readiness_score,
    score - LAG(score) OVER (ORDER BY day) AS change_from_prev_day
FROM daily_readiness
ORDER BY day;
"""

df_readiness = pd.read_sql(readiness_query, engine, parse_dates = ["day"])
st.bar_chart(df_readiness.set_index(("day"))["change_from_prev_day"])

st.subheader("Top 10 Worst Recovery Days (by Resting Heart Rate)")

rank_query = """
SELECT
    day,
    resting_heart_rate,
    RANK() OVER (ORDER BY resting_heart_rate ASC) AS hr_rank
FROM daily_readiness
WHERE resting_heart_rate IS NOT NULL
ORDER BY hr_rank
LIMIT 10;
"""

df_rank = pd.read_sql(rank_query, engine, parse_dates = ["day"])
st.dataframe(df_rank, hide_index = True)