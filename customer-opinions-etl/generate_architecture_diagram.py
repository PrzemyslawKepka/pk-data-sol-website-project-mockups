"""
Generate an architecture diagram for the Customer Opinions ETL Pipeline.
Shows multi-layer architecture: Data Sources -> Staging -> Production -> Consumers
All orchestrated by Apache Airflow.
"""

import os

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.storage import Storage
from diagrams.onprem.analytics import Tableau
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python

# Custom icon path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = "custom-icons"
TERADATA_ICON = os.path.join(SCRIPT_DIR, ICON_DIR, "id63eny4V8_1769062761471.png")

# Output settings
OUTPUT_FILENAME = "customer_opinions_etl_architecture"
GRAPH_ATTR = {
    "fontsize": "20",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "ortho",
    "label": "Customer Opinions ETL Pipeline",
    "labelloc": "t",
}


def generate_diagram():
    """Generate the ETL pipeline architecture diagram."""

    with Diagram(
        filename=OUTPUT_FILENAME,
        show=False,
        direction="LR",
        graph_attr=GRAPH_ATTR,
    ):
        # Orchestration layer - Airflow at the top
        with Cluster("Orchestration"):
            airflow = Airflow("Apache Airflow\nScheduler & DAGs")

        # Data Sources Layer (leftmost)
        with Cluster("Data Sources"):
            with Cluster("External APIs"):
                survey_api = Internet("Survey\nProvider API")

            with Cluster("File Sources"):
                sftp_server = Storage("SFTP Server\n(Partner Data)")
                csv_files = Storage("CSV Files\n(Manual Uploads)")

        # ETL Processing Layer
        with Cluster("ETL Processing"):
            python_etl = Python("Python ETL\n(Factory Pattern\nMultithreading)")

        # Database Layer
        with Cluster("Teradata Database"):
            with Cluster("Staging Zone"):
                stg_surveys = Custom("stg_surveys", TERADATA_ICON)
                stg_social = Custom("stg_social_media", TERADATA_ICON)
                stg_partner = Custom("stg_partner_data", TERADATA_ICON)

            with Cluster("Production Zone"):
                prod_opinions = Custom("fact_customer_opinions", TERADATA_ICON)
                prod_nps = Custom("fact_nps_scores", TERADATA_ICON)
                dim_customers = Custom("dim_customers", TERADATA_ICON)

            with Cluster("Data Marts / Views"):
                vw_sentiment = Custom("vw_sentiment_analysis", TERADATA_ICON)
                vw_nps_trend = Custom("vw_nps_trends", TERADATA_ICON)

        # Data Consumers Layer (rightmost)
        with Cluster("Data Consumers"):
            data_scientists = Users("Data Scientists\n(ML Models)")
            researchers = Users("UX Researchers\n(Customer Insights)")
            bi_tools = Tableau("BI Dashboards\n(NPS Reports)")

        # Connections - Data flow from sources to staging
        survey_api >> Edge(label="API Pull") >> python_etl
        sftp_server >> Edge(label="SFTP") >> python_etl
        csv_files >> Edge(label="Load") >> python_etl

        # ETL to Staging (EL phase)
        python_etl >> Edge(label="Extract & Load") >> stg_surveys
        python_etl >> stg_social
        python_etl >> stg_partner

        # Staging to Production (T phase - SQL transformations)
        stg_surveys >> Edge(label="SQL Transform", style="dashed") >> prod_opinions
        stg_social >> Edge(style="dashed") >> prod_opinions
        stg_partner >> Edge(style="dashed") >> prod_opinions

        prod_opinions >> prod_nps
        prod_opinions >> dim_customers

        # Production to Views
        prod_opinions >> vw_sentiment
        prod_nps >> vw_nps_trend

        # Views to Consumers
        vw_sentiment >> data_scientists
        vw_sentiment >> researchers
        vw_nps_trend >> bi_tools

        # Airflow orchestrates everything
        airflow >> Edge(label="Schedules", style="dotted") >> python_etl


if __name__ == "__main__":
    generate_diagram()
    print(f"Diagram generated: {OUTPUT_FILENAME}.png")
