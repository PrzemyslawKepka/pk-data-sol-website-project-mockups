"""
Streamlit Center & Standards - Mockup App
A visual cookiecutter for Streamlit project generation and guidelines hub.
"""

import streamlit as st

st.set_page_config(
    page_title="Streamlit Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar info
with st.sidebar:
    st.header("📚 Quick Links")
    st.markdown("""
    - [Streamlit Documentation](https://docs.streamlit.io)
    - [Internal Wiki](#)
    - [Submit Feedback](#)
    """)

    st.divider()

    st.header("📊 Statistics")
    st.metric("Projects Generated", "47")
    st.metric("Active Applications", "14")

# Main page - Project Generator
st.title("🚀 Streamlit Center")
st.markdown("### Your hub for Streamlit development standards and project scaffolding")

st.divider()

st.header("📦 Project Generator")
st.markdown(
    "Configure your new Streamlit project and generate a ready-to-use template."
)

with st.form("project_generator"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Basic Configuration")
        project_name = st.text_input(
            "Project Name",
            placeholder="my-streamlit-app",
            help="Use lowercase with hyphens (e.g., sales-dashboard)",
        )

        project_description = st.text_area(
            "Project Description",
            placeholder="A brief description of your application...",
            height=100,
        )

        author_name = st.text_input("Author Name", placeholder="Your name or team name")

        python_version = st.selectbox(
            "Python Version",
            options=["3.11", "3.10", "3.9", "3.12"],
            index=0,
            help="Recommended: 3.11 for best compatibility",
        )

    with col2:
        st.subheader("Project Structure")
        num_pages = st.number_input(
            "Number of Pages",
            min_value=1,
            max_value=10,
            value=3,
            help="How many pages should your app have?",
        )

        page_names = st.text_input(
            "Page Names (comma-separated)",
            placeholder="Dashboard, Analytics, Settings",
            help="Leave empty for default page names",
        )

        include_auth = st.checkbox(
            "Include Authentication Module",
            value=True,
            help="Adds LDAP/JWT authentication boilerplate",
        )

        include_database = st.checkbox(
            "Include Database Connection",
            value=False,
            help="Adds database connection templates",
        )

        include_charts = st.checkbox(
            "Include Charts Examples",
            value=True,
            help="Adds Plotly/Altair chart templates",
        )

        deployment_target = st.selectbox(
            "Deployment Target",
            options=["Posit Connect", "Docker", "Local Development", "Streamlit Cloud"],
            index=0,
        )

    st.divider()

    # st.subheader("Advanced Options")
    # col3, col4 = st.columns(2)

    # with col3:
    #     use_session_state = st.checkbox("Use Session State Pattern", value=True)
    #     use_caching = st.checkbox("Include Caching Examples", value=True)
    #     use_secrets = st.checkbox("Include Secrets Template", value=True)

    # with col4:
    #     use_testing = st.checkbox("Include Test Structure", value=False)
    #     use_ci_cd = st.checkbox("Include CI/CD Pipeline", value=False)
    #     use_logging = st.checkbox("Include Logging Configuration", value=True)

    # st.divider()

    # Submit button
    submitted = st.form_submit_button(
        "🎉 Generate .ZIP Project", use_container_width=True, type="primary"
    )

    if submitted:
        if not project_name:
            st.error("Please enter a project name!")
        else:
            # Show success message and balloons
            st.success(f"Project '{project_name}' generated successfully!")
            st.balloons()

            # Mock download button (in real app this would generate actual ZIP)
            st.info("📁 Your project template is ready for download!")
            st.download_button(
                label="⬇️ Download Project ZIP",
                data=b"mock_zip_content",  # Mock content for screenshot
                file_name=f"{project_name}.zip",
                mime="application/zip",
            )
