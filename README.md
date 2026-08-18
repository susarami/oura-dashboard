# Oura Health Dashboard

An ongoing personal project that pulls data from the Oura API into a local
SQLite database and applies ETL processes to analyze sleep, readiness, and
activity patterns, with a focus on how shift work affects recovery.

## Requirements

- An Oura Ring and a Personal Access Token (from
  [cloud.ouraring.com/personal-access-tokens](https://cloud.ouraring.com/personal-access-tokens))
- A ServerLife tip tracker CSV export, used to determine actual worked days
  (replaces an earlier weekday based assumption)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # paste your Oura token into .env
python main.py                     # pulls Oura data into data/oura.db
python ingest_work_shifts.py       # loads data/servelife_export.csv into work_shifts
streamlit run dashboard.py
```

Drop your ServerLife CSV export in `data/servelife_export.csv` before running
the ingestion step.

## What's inside

Four SQLite tables, populated via a Python ETL pipeline:
- **daily_sleep** — score, deep sleep, efficiency, latency, REM, restfulness, timing, total sleep
- **daily_readiness** — score, temperature deviation, recovery index, HRV balance, sleep regularity, resting heart rate score
- **daily_activity** — score, steps, high/medium/low activity time, sedentary time, recovery time
- **work_shifts** — actual worked days pulled from a ServerLife tip tracker export, with hours worked, tip amount, and hourly wage

The dashboard includes rolling 7-day averages, work-schedule correlation
analysis, and a correlation heatmap across all three Oura tables. Oura data
is filtered to the date range covered by the ServerLife export, so stats
only reflect days where a work shift is actually confirmed or ruled out.

## Notable findings

Comparing metrics on days following a confirmed work shift (from
`work_shifts`) vs. confirmed days off:

- Sleep efficiency is lower after work days, but the difference did not
  reach significance (t = -1.43, p = 0.153)
- Recovery time score is lower after work days (t = -2.79, p = 0.0056)
- Resting heart rate recovery score is lower after work days, though not
  significant at this sample size (t = -1.59, p = 0.112)

On the work day itself, activity is strongly correlated with the day type,
steps and low-intensity activity time rise, sedentary time drops sharply
(correlation coefficients of 0.75 to 0.90 with `is_workday`).

**Does the effect compound after back-to-back shifts?**
Days were grouped by how many of the previous two days were confirmed work
days (0, 1, or 2) and compared with a one-way ANOVA:

- Recovery time drops in a clear step pattern (99.3 → 98.7 → 95.3), strongly
  significant (F = 14.03, p < 0.0001)

Recovery time appears to be the metric most sensitive to accumulated
fatigue from back-to-back shifts.

**Data quality note:** Oura's Rest Mode zeroes out `activity_score` during
illness. These stretches are detected and treated as missing data rather
than real low-activity days.