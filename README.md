# E-Commerce Customer Segmentation

A small Streamlit project that groups customers by their shopping activity. It uses Recency, Frequency, and Monetary (RFM) values with K-Means clustering.

## What the app does
- Reads an Excel or CSV transaction file.
- Removes rows without a customer ID and rows with missing details, negative quantities, or non-positive prices.
- Calculates each customer's Recency, Frequency, and Monetary values.
- Lets you choose how many customer groups to create.
- Shows group sizes and typical values for each group.
- Downloads the customer results as a CSV file.

## Data

The app expects these columns: `InvoiceNo`, `Quantity`, `InvoiceDate`, `UnitPrice`, and `CustomerID`.

You can get the Online Retail dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail). The dataset is not included in this repository; upload it in the app after it starts.

## Run the app

1. Install Python and open this project folder in VS Code.
2. In VS Code, choose **Terminal → New Terminal**.
3. Install the packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

5. Upload your Excel or CSV file in the browser page that opens.

If `python` is not recognized, replace it with the Python interpreter path selected in VS Code.

## What the measures mean

- **Recency:** days since the customer's last purchase. A lower number means a more recent purchase.
- **Frequency:** number of different invoices (orders).
- **Monetary:** total spending, calculated as quantity times unit price.

The group numbers are just labels. Compare the values in the results table to understand the groups. Try different group counts and compare the results before making conclusions.
