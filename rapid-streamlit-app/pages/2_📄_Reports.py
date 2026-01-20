"""
Reports - Generate and Export Usage Reports
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="centered",
)

st.title("📄 Generate Reports")
st.markdown("Export usage data and eligibility check reports.")

st.divider()

# Report type selection
st.subheader("📊 Report Configuration")

report_type = st.selectbox(
    "Report Type",
    options=[
        "Daily Usage Summary",
        "User Activity Report",
        "Eligibility Statistics",
        "Error Log Export",
        "Branch Performance"
    ]
)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=7)
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now()
    )

# Additional filters based on report type
st.markdown("**Filters**")

col1, col2 = st.columns(2)

with col1:
    branch_filter = st.multiselect(
        "Branch",
        options=["All Branches", "Warsaw Central", "Krakow Main", "Gdansk Port", "Wroclaw HQ", "Poznan City"],
        default=["All Branches"]
    )

with col2:
    user_filter = st.text_input(
        "User ID (optional)",
        placeholder="Leave empty for all users"
    )

format_option = st.radio(
    "Export Format",
    options=["Excel (.xlsx)", "CSV (.csv)", "PDF Report"],
    horizontal=True
)

st.divider()

# Generate button
if st.button("📥 Generate Report", type="primary", use_container_width=True):
    with st.spinner("Generating report..."):
        import time
        time.sleep(1)

    st.success("Report generated successfully!")

    # Show preview
    st.subheader("📋 Report Preview")

    if report_type == "Daily Usage Summary":
        preview_data = {
            "Date": ["2024-01-19", "2024-01-18", "2024-01-17", "2024-01-16", "2024-01-15"],
            "Total Queries": [1247, 1320, 1189, 1245, 987],
            "Unique Users": [89, 92, 85, 88, 78],
            "Avg Response (ms)": [823, 812, 856, 798, 834],
            "Error Count": [4, 2, 5, 3, 6]
        }
    elif report_type == "User Activity Report":
        preview_data = {
            "User ID": ["J.KOWALSKI", "M.NOWAK", "A.WISNIEWSKI", "K.WOJCIK", "P.KAMINSKI"],
            "Total Queries": [1245, 1102, 987, 876, 765],
            "Eligible Results": [1089, 956, 845, 756, 678],
            "Not Eligible": [156, 146, 142, 120, 87],
            "Branch": ["Warsaw Central", "Krakow Main", "Gdansk Port", "Warsaw Central", "Wroclaw HQ"]
        }
    elif report_type == "Eligibility Statistics":
        preview_data = {
            "Product": ["Cash Loan", "Credit Card", "Mortgage Refinancing", "Investment Products", "Insurance"],
            "Queries": [2456, 1987, 892, 1234, 567],
            "Eligible %": ["78.3%", "82.1%", "34.5%", "91.2%", "88.7%"],
            "Not Eligible %": ["21.7%", "17.9%", "65.5%", "8.8%", "11.3%"],
            "Trend": ["↑", "↑", "↓", "→", "↑"]
        }
    else:
        preview_data = {
            "Timestamp": ["2024-01-19 14:32:15", "2024-01-19 12:15:42", "2024-01-18 16:45:33"],
            "Type": ["Timeout", "DB Error", "Validation"],
            "User": ["M.NOWAK", "K.WOJCIK", "A.WISNIEWSKI"],
            "Details": ["Query exceeded 30s limit", "Connection pool exhausted", "Invalid client ID format"]
        }

    df_preview = pd.DataFrame(preview_data)
    st.dataframe(df_preview, use_container_width=True, hide_index=True)

    st.caption(f"Showing first 5 rows of {len(df_preview) * 20} total records")

    # Download button
    st.download_button(
        label="⬇️ Download Full Report",
        data=b"mock_report_content",
        file_name=f"report_{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()

# Scheduled reports section
st.subheader("📅 Scheduled Reports")

st.info("Configure automatic report generation and delivery.")

scheduled_data = {
    "Report": ["Daily Usage Summary", "Weekly User Activity", "Monthly Eligibility Stats"],
    "Frequency": ["Daily @ 07:00", "Weekly (Monday)", "Monthly (1st)"],
    "Recipients": ["team@bank.pl", "managers@bank.pl", "analytics@bank.pl"],
    "Status": ["Active", "Active", "Paused"]
}

df_scheduled = pd.DataFrame(scheduled_data)
st.dataframe(df_scheduled, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)
with col1:
    st.button("➕ Add Scheduled Report", use_container_width=True)
with col2:
    st.button("✏️ Manage Schedules", use_container_width=True)
