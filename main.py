import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


st.title("E-Commerce Customer Segmentation")
st.write("Upload a sales file to group customers by their shopping activity.")
st.write("The file should have InvoiceNo, Quantity, InvoiceDate, UnitPrice, and CustomerID columns.")

file = st.file_uploader("Upload your file", type=["xlsx", "xls", "csv"])

if file is not None:
    try:
        if file.name.endswith(".csv"):
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file)
    except Exception:
        st.error("I couldn't open that file. Please check that it is a valid Excel or CSV file.")
        st.stop()

    needed_columns = ["InvoiceNo", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID"]
    missing_columns = []

    for column in needed_columns:
        if column not in data.columns:
            missing_columns.append(column)

    if missing_columns:
        st.error("These columns are missing: " + ", ".join(missing_columns))
        st.stop()

    st.subheader("Data cleaning")
    st.write("Rows in the uploaded file:", len(data))

    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["UnitPrice"] = pd.to_numeric(data["UnitPrice"], errors="coerce")
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")

    clean_data = data.dropna(
        subset=["CustomerID", "InvoiceNo", "Quantity", "UnitPrice", "InvoiceDate"]
    )
    clean_data = clean_data[
        (clean_data["Quantity"] > 0) & (clean_data["UnitPrice"] > 0)
    ].copy()

    if clean_data.empty:
        st.error("There are no usable purchase rows in this file.")
        st.stop()

    st.write("Rows left after cleaning:", len(clean_data))

    clean_data["TotalPrice"] = clean_data["Quantity"] * clean_data["UnitPrice"]

    last_day = clean_data["InvoiceDate"].max() + pd.Timedelta(days=1)
    customers = clean_data.groupby("CustomerID").agg(
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum"),
        LastPurchase=("InvoiceDate", "max"),
    )
    customers["Recency"] = (last_day - customers["LastPurchase"]).dt.days
    customers = customers[["Recency", "Frequency", "Monetary"]]

    if len(customers) < 2:
        st.error("The file needs at least two customers to make groups.")
        st.stop()

    st.subheader("Choose customer groups")
    st.write("Try a few group counts and compare the results.")
    max_groups = min(6, len(customers))
    start_groups = min(4, max_groups)
    group_count = st.slider("Number of groups", 2, max_groups, start_groups)

    scaler = StandardScaler()
    scaled_customers = scaler.fit_transform(customers)

    model = KMeans(n_clusters=group_count, random_state=42, n_init=10)
    customers["Segment"] = model.fit_predict(scaled_customers)

    st.subheader("Results")
    st.write("Customers in each group:")
    group_sizes = customers["Segment"].value_counts().sort_index()
    st.bar_chart(group_sizes)

    st.write("Middle values for each group:")
    group_summary = customers.groupby("Segment")[["Recency", "Frequency", "Monetary"]].median()
    st.dataframe(group_summary.round(2))
    st.caption("Recency is days since last purchase. Frequency is number of orders. Monetary is total spending.")

    st.write("Customer results:")
    st.dataframe(customers.reset_index())

    csv_file = customers.reset_index().to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download customer results",
        data=csv_file,
        file_name="customer_segments.csv",
        mime="text/csv",
    )
else:
    st.write("Upload your file to get started.")
