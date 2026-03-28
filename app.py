import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="DRONA Analytics Dashboard", layout="wide")

st.title("🛡️ MiniEklavyaProto School Analytics Dashboard")
st.markdown("Real-time engagement and adoption metrics for the Eklavya Platform.")

# Database Connection
def get_data(query):
    conn = sqlite3.connect('drona_analytics.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
school_type = st.sidebar.multiselect(
    "Select School Type", 
    options=['Government', 'Private', 'Semi-Government'],
    default=['Government', 'Private', 'Semi-Government']
)

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)

total_users = get_data("SELECT COUNT(*) as count FROM users")['count'][0]
total_sessions = get_data("SELECT COUNT(*) as count FROM sessions")['count'][0]
avg_duration = get_data("SELECT AVG(duration_minutes) as avg FROM sessions")['avg'][0]
active_rate = get_data("SELECT (COUNT(DISTINCT user_id) * 100.0 / (SELECT COUNT(*) FROM users)) as rate FROM sessions")['rate'][0]

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Total Sessions", f"{total_sessions:,}")
col3.metric("Avg. Session", f"{avg_duration:.1f} min")
col4.metric("Active User Rate", f"{active_rate:.1f}%")

st.divider()

# --- CHARTS SECTION ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Daily Active Users (DAU) Trend")
    dau_data = get_data("""
        SELECT date(login_time) as date, COUNT(DISTINCT user_id) as dau 
        FROM sessions GROUP BY 1 ORDER BY 1 ASC
    """)
    fig_dau = px.line(dau_data, x='date', y='dau', template="plotly_white", color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig_dau, use_container_width=True)

with c2:
    st.subheader("Feature Adoption")
    feature_data = get_data("""
        SELECT feature_used, COUNT(*) as usage_count 
        FROM activities GROUP BY 1 ORDER BY 2 DESC
    """)
    fig_feat = px.bar(feature_data, x='usage_count', y='feature_used', orientation='h', color='feature_used')
    st.plotly_chart(fig_feat, use_container_width=True)

# --- SCHOOL LEVEL TABLE ---
st.subheader("School Performance Leaderboard")
school_perf = get_data(f"""
    SELECT 
        s.school_id, 
        s.school_type, 
        s.city, 
        COUNT(DISTINCT u.user_id) as active_students,
        COUNT(sess.session_id) as total_interactions
    FROM schools s
    JOIN users u ON s.school_id = u.school_id
    JOIN sessions sess ON u.user_id = sess.user_id
    WHERE s.school_type IN ({str(school_type)[1:-1]})
    GROUP BY 1, 2, 3
    ORDER BY total_interactions DESC
    LIMIT 10
""")
st.dataframe(school_perf, use_container_width=True)

st.success("Dashboard loaded successfully. All data is simulated based on DRONA platform architecture.")


# app.py ke end mein ye code add karo
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.divider()
st.subheader("🤖 AI-Driven Student Segmentation (K-Means Clustering)")
st.markdown("Using Machine Learning to automatically group students based on engagement patterns to identify **At-Risk** accounts.")

# Get data for clustering
cluster_data = get_data("""
    SELECT 
        u.user_id,
        COUNT(s.session_id) as total_sessions,
        SUM(s.duration_minutes) as total_minutes
    FROM users u
    JOIN sessions s ON u.user_id = s.user_id
    WHERE u.role = 'Student'
    GROUP BY u.user_id
""")

# Prepare and scale data
X = cluster_data[['total_sessions', 'total_minutes']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Run K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_data['Cluster'] = kmeans.fit_predict(X_scaled)

# Map clusters to business logic (Based on centroids)
cluster_mapping = {0: 'Casuals', 1: 'Champions', 2: 'At-Risk'} # Note: You might need to adjust mapping based on actual centroid values
cluster_data['Segment'] = cluster_data['Cluster'].map(cluster_mapping)

# Visualize the AI Output
fig_cluster = px.scatter(
    cluster_data, 
    x='total_sessions', 
    y='total_minutes', 
    color='Segment',
    title="Student Engagement Clusters",
    color_discrete_sequence=['#FFA15A', '#00CC96', '#EF553B']
)
st.plotly_chart(fig_cluster, use_container_width=True)
