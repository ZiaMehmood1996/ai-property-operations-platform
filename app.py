import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="AI Property Operations Platform",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Debug Info
# -----------------------------

st.write("Python Executable:")
st.code(sys.executable)

# -----------------------------
# Header
# -----------------------------

st.title("🏠 AI Property Operations Platform")
st.subheader("Property Management Analytics")

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

# -----------------------------
# File Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# -----------------------------
# Main App
# -----------------------------

if uploaded_file is not None:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # -----------------------------
    # Data Quality Metrics
    # -----------------------------

    rows = df.shape[0]
    cols = df.shape[1]

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    completeness_score = (
        ((rows * cols) - missing_values)
        / (rows * cols)
    ) * 100

    quality_score = (
        completeness_score
        - ((duplicate_rows / rows) * 100)
    )

    quality_score = max(
        0,
        round(quality_score, 2)
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Rows", rows)
    col2.metric("Columns", cols)
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicates", duplicate_rows)
    col5.metric(
        "Quality Score",
        f"{quality_score}%"
    )

    # -----------------------------
    # Dataset Preview
    # -----------------------------

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Column Information
    # -----------------------------

    st.subheader("Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        info_df,
        use_container_width=True
    )

    # -----------------------------
    # Data Quality Summary
    # -----------------------------

    st.subheader("Data Quality Summary")

    quality_df = pd.DataFrame({
        "Metric": [
            "Completeness Score",
            "Duplicate Rows"
        ],
        "Value": [
            round(completeness_score, 2),
            duplicate_rows
        ]
    })

    st.dataframe(
        quality_df,
        use_container_width=True
    )

    # -----------------------------
    # KPI Dashboard
    # -----------------------------

    total_revenue = (
        df["Revenue"].sum()
        if "Revenue" in df.columns
        else 0
    )

    avg_occupancy = (
        round(df["Occupancy"].mean(), 2)
        if "Occupancy" in df.columns
        else 0
    )

    total_bookings = (
        df["Bookings"].sum()
        if "Bookings" in df.columns
        else 0
    )

    top_property = "N/A"

    if (
        "Property" in df.columns
        and "Revenue" in df.columns
    ):
        top_property = df.loc[
            df["Revenue"].idxmax(),
            "Property"
        ]

    st.subheader("📊 KPI Dashboard")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

    kpi2.metric(
        "Average Occupancy",
        f"{avg_occupancy}%"
    )

    kpi3.metric(
        "Total Bookings",
        total_bookings
    )

    kpi4.metric(
        "Top Property",
        top_property
    )

    # -----------------------------
    # Revenue Chart
    # -----------------------------

    if (
        "Property" in df.columns
        and "Revenue" in df.columns
    ):

        st.subheader("📈 Revenue by Property")

        fig = px.bar(
            df,
            x="Property",
            y="Revenue",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Occupancy Chart
    # -----------------------------

    if (
        "Property" in df.columns
        and "Occupancy" in df.columns
    ):

        st.subheader("🏠 Occupancy by Property")

        fig2 = px.bar(
            df,
            x="Property",
            y="Occupancy",
            text_auto=True
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # -----------------------------
    # Property Ranking
    # -----------------------------

    if (
        "Property" in df.columns
        and "Revenue" in df.columns
    ):

        st.subheader("🏆 Property Revenue Ranking")

        ranking_df = (
            df.groupby("Property")["Revenue"]
            .sum()
            .reset_index()
            .sort_values(
                by="Revenue",
                ascending=False
            )
        )

        ranking_df.insert(
            0,
            "Rank",
            range(
                1,
                len(ranking_df) + 1
            )
        )

        st.dataframe(
            ranking_df,
            use_container_width=True
        )

    # -----------------------------
    # Property Health Score
    # -----------------------------

    if all(
        col in df.columns
        for col in [
            "Property",
            "Revenue",
            "Occupancy",
            "Bookings"
        ]
    ):

        st.subheader(
            "💚 Property Health Score"
        )

        health_df = df[
            [
                "Property",
                "Revenue",
                "Occupancy",
                "Bookings"
            ]
        ].copy()

        health_df["Health Score"] = (
            (health_df["Revenue"] /
             health_df["Revenue"].max()) * 40
            +
            (health_df["Occupancy"] / 100) * 40
            +
            (health_df["Bookings"] /
             health_df["Bookings"].max()) * 20
        ).round(0)

        health_df = health_df.sort_values(
            by="Health Score",
            ascending=False
        )

        st.dataframe(
            health_df[
                [
                    "Property",
                    "Health Score"
                ]
            ],
            use_container_width=True
        )

    # -----------------------------
    # Executive Summary
    # -----------------------------

    st.subheader("📋 Executive Summary")

    summary = f"""
Total portfolio revenue is ${total_revenue:,.0f}.

Average occupancy rate is {avg_occupancy}%.

Total bookings recorded: {total_bookings}.

Top performing property: {top_property}.

Key Recommendation:
Focus marketing efforts on lower-performing properties and analyze factors driving the success of the top property.
"""

    st.info(summary)


    st.subheader("📥 Export Report")

    csv = health_df.to_csv(index=False)

    st.download_button(
        label="Download Health Score Report",
        data=csv,
        file_name="property_health_report.csv",
        mime="text/csv"
    )