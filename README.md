# Oura Health Dashboard

An ongoing personal project that pulls data from the Oura API into a local
SQLite database and applies ETL processes to analyze sleep, readiness, and
activity patterns — with a focus on how shift work affects recovery.

## Requirements

- An Oura Ring and a Personal Access Token (from
  [cloud.ouraring.com/personal-access-tokens](https://cloud.ouraring.com/personal-access-tokens))

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # paste your Oura token into .env
python main.py          # pulls Oura data into data/oura.db
streamlit run dashboard.py
```

## What's inside

Three SQLite tables, populated via a Python ETL pipeline:
- **daily_sleep** — score, deep sleep, efficiency, latency, REM, restfulness, timing, total sleep
- **daily_readiness** — score, temperature deviation, recovery index, HRV balance, sleep regularity, resting heart rate score
- **daily_activity** — score, steps, high/medium/low activity time, sedentary time, recovery time

The dashboard includes rolling 7-day averages, work-schedule correlation
analysis, and a correlation heatmap across all three tables.

## Notable findings

Comparing metrics on days following a work shift (Tue/Sat/Sun) vs. days off:

- Sleep efficiency is lower after work days (t = -2.46, p = 0.014)
- Recovery time score is lower after work days (t = -3.06, p = 0.002)
- Resting heart rate recovery score is lower after work days (t = -4.68, p < 0.0001)

On the work day itself, activity is strongly correlated with the day type —
steps and low-intensity activity time rise, sedentary time drops sharply
(correlation coefficients of 0.7–0.8 with `is_workday`).

**Does the effect compound after back-to-back shifts (Sat + Sun)?**
Since two of the three work days fall on consecutive days, days were grouped
by how many of the previous two days were work days (0, 1, or 2) and
compared with a one-way ANOVA:

- Recovery time drops in a clear step pattern (99.5 → 98.3 → 95.1) —
  strongly significant (F = 13.16, p < 0.0001)
- Sleep score shows a similar but weaker pattern — did not reach
  significance (F = 2.51, p = 0.083), likely due to limited sample size
  for the double-shift group (n = 48)
- Resting heart rate recovery score showed no clear compounding pattern
  (F = 0.94, p = 0.39)

Recovery time appears to be the metric most sensitive to accumulated
fatigue from back-to-back shifts; the effect is less conclusive for sleep
score and not evident for resting heart rate score at this sample size.


**Data quality note:** Oura's Rest Mode zeroes out `activity_score` during
illness. These stretches are detected and treated as missing data rather
than real low-activity days.
