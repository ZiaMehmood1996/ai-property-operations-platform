import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Property Operations Platform",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AI Property Operations Platform")

st.subheader("Property Management Analytics")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

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

    quality_score = max(0, round(quality_score, 2))

    # Dashboard Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Rows", rows)
    col2.metric("Columns", cols)
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicates", duplicate_rows)
    col5.metric("Quality Score", f"{quality_score}%")

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

    st.dataframe(info_df)

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

    st.dataframe(quality_df)

    # -----------------------------
    # KPI Dashboard
    # -----------------------------

    if "Revenue" in df.columns:
        total_revenue = df["Revenue"].sum()
    else:
        total_revenue = 0

    if "Occupancy" in df.columns:
        avg_occupancy = round(df["Occupancy"].mean(), 2)
    else:
        avg_occupancy = 0

    if "Bookings" in df.columns:
        total_bookings = df["Bookings"].sum()
    else:
        total_bookings = 0

    top_property = "N/A"

    if "Property" in df.columns and "Revenue" in df.columns:
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

    if "Property" in df.columns and "Revenue" in df.columns:

        st.subheader("📈 Revenue by Property")

        fig = px.bar(
            df,
            x="Property",
            y="Revenue",
            title="Revenue by Property",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Occupancy Chart
    # -----------------------------

    if "Property" in df.columns and "Occupancy" in df.columns:

        st.subheader("🏠 Occupancy by Property")

        fig2 = px.bar(
            df,
            x="Property",
            y="Occupancy",
            title="Occupancy by Property",
            text_auto=True
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )