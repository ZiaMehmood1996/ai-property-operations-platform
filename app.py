if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

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

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Rows", rows)
    col2.metric("Columns", cols)
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicates", duplicate_rows)
    col5.metric("Quality Score", f"{quality_score}%")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(info_df)

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