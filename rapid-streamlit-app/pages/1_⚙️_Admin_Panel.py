"""
Admin Panel - Usage Statistics and Monitoring
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Admin Panel")
st.markdown("Monitor application usage and performance metrics.")

st.divider()

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Queries Today",
        value="1,247",
        delta="↑ 12%",
    )

with col2:
    st.metric(
        label="Active Users",
        value="89",
        delta="↑ 5",
    )

with col3:
    st.metric(
        label="Avg Response Time",
        value="0.8s",
        delta="-0.2s",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Error Rate",
        value="0.3%",
        delta="-0.1%",
        delta_color="inverse"
    )

st.divider()

# Usage over time
st.subheader("📈 Query Volume (Last 7 Days)")

# Generate mock data for chart
dates = [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(6, -1, -1)]
queries = [890, 1102, 987, 1245, 1189, 1320, 1247]

chart_data = pd.DataFrame({
    "Date": dates,
    "Queries": queries
})

st.bar_chart(chart_data.set_index("Date"))

st.divider()

# Recent queries log
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Recent Queries")

    log_data = {
        "Timestamp": [
            "2024-01-19 14:32:15",
            "2024-01-19 14:31:58",
            "2024-01-19 14:31:42",
            "2024-01-19 14:31:28",
            "2024-01-19 14:31:05",
            "2024-01-19 14:30:51",
            "2024-01-19 14:30:33",
        ],
        "User": [
            "J.KOWALSKI",
            "M.NOWAK",
            "A.WISNIEWSKI",
            "K.WOJCIK",
            "J.KOWALSKI",
            "P.KAMINSKI",
            "M.NOWAK",
        ],
        "Client ID": [
            "98765432101",
            "12345678901",
            "55566677788",
            "11122233344",
            "99988877766",
            "44455566677",
            "33344455566",
        ],
        "Response (ms)": [
            "823",
            "756",
            "912",
            "689",
            "801",
            "734",
            "867",
        ],
        "Status": [
            "Success",
            "Success",
            "Success",
            "Success",
            "Success",
            "Success",
            "Error",
        ]
    }

    df_log = pd.DataFrame(log_data)
    st.dataframe(df_log, use_container_width=True, hide_index=True)

with col2:
    st.subheader("👥 Top Users Today")

    users_data = {
        "User": ["J.KOWALSKI", "M.NOWAK", "A.WISNIEWSKI", "K.WOJCIK", "P.KAMINSKI"],
        "Queries": [156, 142, 128, 115, 98]
    }

    df_users = pd.DataFrame(users_data)
    st.dataframe(df_users, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("🏢 Branch Activity")
    branch_data = {
        "Branch": ["Warsaw Central", "Krakow Main", "Gdansk Port", "Wroclaw HQ"],
        "Queries": [423, 312, 287, 225]
    }

    df_branch = pd.DataFrame(branch_data)
    st.dataframe(df_branch, use_container_width=True, hide_index=True)

st.divider()

# System status
st.subheader("🖥️ System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Database Connection**")
    st.markdown("🟢 Connected")
    st.caption("Last check: 2 min ago")

with col2:
    st.markdown("**ETL Pipeline**")
    st.markdown("🟢 Running")
    st.caption("Last sync: 06:00 AM")

with col3:
    st.markdown("**Cache Status**")
    st.markdown("🟢 Active")
    st.caption("Hit rate: 94%")
