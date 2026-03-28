import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ── CONFIG ────────────────────────────────────────────────────────────────────
NUM_SCHOOLS    = 50
NUM_USERS      = 5_000
NUM_SESSIONS   = 50_000
NUM_ACTIVITIES = 150_000
START_DATE     = datetime(2025, 9, 1)

# FIX 2: Seed BOTH numpy and python's random for full reproducibility
np.random.seed(42)
random.seed(42)

print("Generating DRONA EdTech Dataset...")

# ── 1. SCHOOLS TABLE (new — needed for school-level analysis) ─────────────────
# FIX 8: Added school dimension so school-level aggregation queries work
school_ids   = [f"SCH{str(i).zfill(3)}" for i in range(1, NUM_SCHOOLS + 1)]
school_types = np.random.choice(
    ['Government', 'Private', 'Semi-Government'],
    p=[0.50, 0.35, 0.15],
    size=NUM_SCHOOLS
)
school_cities = np.random.choice(
    ['Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Meerut', 'Allahabad'],
    size=NUM_SCHOOLS
)
schools_df = pd.DataFrame({
    'school_id'  : school_ids,
    'school_type': school_types,
    'city'       : school_cities,
    'onboarded_date': [
        START_DATE + timedelta(days=random.randint(-90, 0))
        for _ in range(NUM_SCHOOLS)
    ]
})

# ── 2. USERS TABLE ────────────────────────────────────────────────────────────
user_ids  = [f"U{str(i).zfill(5)}" for i in range(1, NUM_USERS + 1)]
roles     = np.random.choice(
    ['Student', 'Teacher', 'Admin'],
    p=[0.85, 0.13, 0.02],
    size=NUM_USERS
)
statuses  = np.random.choice(
    ['Active', 'Inactive', 'Suspended'],
    p=[0.90, 0.08, 0.02],
    size=NUM_USERS
)
reg_dates = [
    START_DATE + timedelta(days=random.randint(0, 180))
    for _ in range(NUM_USERS)
]
# Assign each user to a school
user_school_ids = np.random.choice(school_ids, size=NUM_USERS)

users_df = pd.DataFrame({
    'user_id'          : user_ids,
    'school_id'        : user_school_ids,
    'role'             : roles,
    'registration_date': reg_dates,
    'status'           : statuses,
})

# ── 3. SESSIONS TABLE ─────────────────────────────────────────────────────────
# FIX 4: Only Active users generate sessions (realistic behaviour)
active_user_ids  = users_df[users_df['status'] == 'Active']['user_id'].tolist()
session_ids      = [f"S{str(i).zfill(6)}" for i in range(1, NUM_SESSIONS + 1)]
session_user_ids = np.random.choice(active_user_ids, size=NUM_SESSIONS)

devices = np.random.choice(
    ['Mobile', 'Desktop', 'Tablet', np.nan],
    p=[0.60, 0.30, 0.08, 0.02],
    size=NUM_SESSIONS
)

# FIX 1 + FIX 3: Use one random_days variable; clip hour to 0-23 safely
session_starts = []
for _ in range(NUM_SESSIONS):
    day_offset = random.randint(0, 180)
    # Clip to [0,23] instead of % 24 to avoid negative modulo bias
    hour = int(np.clip(np.random.normal(14, 4), 0, 23))
    session_starts.append(
        START_DATE + timedelta(
            days=day_offset,
            hours=hour,
            minutes=random.randint(0, 59)
        )
    )

# Session duration: weighted so longer sessions are less common (realistic)
durations_min = np.random.choice(
    range(5, 121),
    p=np.exp(-np.arange(116) / 40) / np.exp(-np.arange(116) / 40).sum(),
    size=NUM_SESSIONS
)

sessions_df = pd.DataFrame({
    'session_id' : session_ids,
    'user_id'    : session_user_ids,
    'login_time' : session_starts,
    'device_type': devices,
})
sessions_df['logout_time'] = sessions_df['login_time'] + pd.to_timedelta(durations_min, unit='m')
sessions_df['duration_minutes'] = durations_min  # pre-computed — useful for SQL queries

# ── 4. FEATURE ACTIVITIES TABLE ───────────────────────────────────────────────
features = ['Video Lecture', 'Quiz Attempt', 'Assignment Submit', 'Discussion Forum', 'Notes Download']

# FIX 7: Weight activity sampling by session duration — longer sessions → more activities
session_weights = sessions_df['duration_minutes'].values.astype(float)
session_weights /= session_weights.sum()  # normalise to probabilities

activity_session_ids = np.random.choice(
    session_ids,
    size=NUM_ACTIVITIES,
    p=session_weights       # longer sessions attract more activity rows
)

activities_df = pd.DataFrame({
    'activity_id'      : [f"A{str(i).zfill(6)}" for i in range(1, NUM_ACTIVITIES + 1)],
    'session_id'       : activity_session_ids,
    'feature_used'     : np.random.choice(features, p=[0.40, 0.25, 0.15, 0.10, 0.10], size=NUM_ACTIVITIES),
    'time_spent_seconds': np.random.randint(10, 3600, size=NUM_ACTIVITIES),
})

# ── 5. EXPORT ─────────────────────────────────────────────────────────────────
schools_df.to_csv('drona_schools.csv',    index=False)
users_df.to_csv('drona_users.csv',        index=False)
sessions_df.to_csv('drona_sessions.csv',  index=False)
activities_df.to_csv('drona_activities.csv', index=False)

print("\nSuccess! Created 4 datasets:")
print(f"  drona_schools.csv    -> {len(schools_df):>7,} rows")
print(f"  drona_users.csv      -> {len(users_df):>7,} rows")
print(f"  drona_sessions.csv   -> {len(sessions_df):>7,} rows")
print(f"  drona_activities.csv -> {len(activities_df):>7,} rows")
print(f"\nTotal rows: {len(schools_df)+len(users_df)+len(sessions_df)+len(activities_df):,}")
print("\nQuick sanity checks:")
print(f"  Active users only in sessions: {sessions_df['user_id'].isin(active_user_ids).all()}")
print(f"  Negative durations: {(sessions_df['duration_minutes'] < 0).sum()}")
print(f"  Sessions with NaN device: {sessions_df['device_type'].isna().sum()} ({sessions_df['device_type'].isna().mean()*100:.1f}%)")
print(f"  Schools in dataset: {schools_df['school_id'].nunique()}")