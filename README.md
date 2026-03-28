# 🛡️ MiniEklavyaProto: EdTech Product Analytics & AI Segmentation

**A full-stack data pipeline and interactive dashboard simulating real-world engagement metrics for the Eklavya (DRONA) ecosystem.**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.0-07405E?style=flat-square&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)

---

## 🚀 Project Overview
**MiniEklavyaProto** is designed to solve a critical B2B EdTech challenge: **Quantifying user value and predicting churn at the school level.** Unlike generic Kaggle projects, this system generates and analyzes a relational dataset of **200,000+ records** to mirror the actual "DRONA" platform architecture. It transitions from raw telemetry data to actionable business insights using SQL and Unsupervised Machine Learning.

## 🧠 Key Features & Technical Highlights

### 1. Robust Data Engineering
* **Synthetic Telemetry Generation:** Engineered a realistic data generator that models student/teacher behavior, including time-of-day login biases and activity-duration correlation.
* **Relational Schema:** Implemented a 4-table SQLite architecture (`Schools`, `Users`, `Sessions`, `Activities`) to demonstrate mastery of complex JOINs and data integrity.

### 2. Product Analytics (SQL-Driven)
* **Stickiness Metrics:** Authored CTE-based queries to calculate **DAU/MAU ratios**, the "Gold Standard" for SaaS platform health.
* **Feature Adoption Tracking:** Analyzed usage distribution across modules (Video Lectures, Quizzes, Notes) to identify high-value features.

### 3. AI-Driven User Segmentation
* **K-Means Clustering:** Integrated a Scikit-Learn pipeline to segment students into three behavioral cohorts:
    * **Champions:** High-frequency, high-duration power users.
    * **Casuals:** Moderate engagement patterns.
    * **At-Risk:** Low-interaction users requiring immediate intervention.

---

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **Data Handling:** Pandas, NumPy
* **Database:** SQLite3
* **Machine Learning:** Scikit-Learn (K-Means Clustering, StandardScaler)
* **Dashboarding:** Streamlit, Plotly Express

---

## 📈 Dashboard Preview
The interactive dashboard provides:
1. **KPI Scorecards:** Instant visibility into Total Users, Active Rate, and Avg. Session Length.
2. **Engagement Trends:** Time-series analysis of Daily Active Users.
3. **School Leaderboard:** B2B performance ranking by city and school type.
4. **Behavioral Clusters:** Visual AI breakdown of user segments.

---

## ⚙️ Installation & Usage

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/yourusername/MiniEklavyaProto.git](https://github.com/yourusername/MiniEklavyaProto.git)
   cd MiniEklavyaProto
