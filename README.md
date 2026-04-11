# 📦 Chainpulse : Supply Chain Bottleneck Analytics

## 📌 Project Overview

This project focuses on identifying and analyzing **supply chain bottlenecks** using data-driven insights. By comparing actual shipping times against scheduled timelines, this analysis pinpointed delays across different shipping modes, markets, and product categories. The goal is to provide actionable intelligence to optimize logistics efficiency and enhance customer satisfaction.

## 📊 Dataset Description

The analysis uses the **DataCo Smart Supply Chain Dataset**, which includes typical supply chain activities such as provisioning, production, sales, and commercial distribution.

  - **Key Features Used:**
      - `Days for shipping (real)`: The actual time taken to deliver.
      - `Days for shipment (scheduled)`: The promised delivery time.
      - `Shipping Mode`: Standard Class, First Class, Second Class, Same Day.
      - `Market`: Pacific Asia, USCA, Africa, Europe, LATAM.
      - `Order Status`: Status of the order delivery.
      - `Product Price` & `Category Name`: Details regarding the items sold.

## 🛠️ Tech Stack

  * **Language:** Python
  * **Libraries:** \* `Pandas`: Data manipulation and cleaning.
      * `Matplotlib` & `Seaborn`: Advanced data visualization.
      * `NumPy`: Numerical operations.
      * `Streamlit` (Imported for future dashboard integration).

## 🚀 Key Insights from Analysis

Based on the notebook execution, the following findings were discovered:

1.  **High Bottleneck Rate:** Approximately **57.28%** of all orders experienced a bottleneck (Actual days \> Scheduled days).
2.  **Mode Inefficiency:** "Second Class" shipping showed the highest average shipment delay (\~1.99 days), while "Standard Class" was the most reliable relative to its schedule.
3.  **Risk Categories:** Products in the *Golf Bags & Carts* and *Soccer* categories are most prone to shipping delays.
4.  **Market Variance:** Specific markets like *LATAM* and *Pacific Asia* show wider variance in shipping times compared to *USCA*.

## 📂 Project Structure

```bash
├── scba.ipynb                    # Main Jupyter Notebook with analysis & plots
├── Data/
│   └── DataCoSupplyChainDataset.csv  # Raw Input Data (Source)
├── Processed_Supply_Chain_Data.csv # Cleaned data exported after analysis
└── README.md                     # Project documentation
```

## ⚙️ Data Pipeline

1.  **Data Cleaning:** \* Handling missing values in `Customer Zipcode` and `Product Description`.
      * Converting `order_date` and `shipment_date` to datetime objects.
      * Stripping whitespace from column headers for consistent indexing.
2.  **Feature Engineering:**
      * `Shipment_Delay`: Calculated as `Real Days - Scheduled Days`.
      * `Is_Bottleneck`: Boolean flag indicating if a delay occurred.
      * `Internal_Processing_Time`: Time difference between order date and shipment date.
3.  **Exploratory Data Analysis (EDA):**
      * Distribution of shipping days across different markets.
      * Correlation analysis between Product Price and Shipping Speed.
      * Proportion analysis using Donut charts and Countplots.

## 📈 Visualizations Included

  * **Bottleneck Proportion:** A donut chart showing the split between on-time and delayed orders.
  * **Shipping Mode Impact:** Countplots comparing bottlenecks across various logistics tiers.
  * **Market Distribution:** Violin plots showing the density and quartiles of shipping durations per global market.
  * **Regression Analysis:** Scatter plots identifying if higher product prices correlate with faster shipping.

## 🏗️ How to Run

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/MTank76/Supply-Chain-Bottleneck-Analysis.git
    ```
2.  **Install Dependencies:**
    ```bash
    pip install pandas matplotlib seaborn numpy
    ```
3.  **Run the Notebook:**
    Open `scba.ipynb` in Jupyter Notebook or VS Code and run all cells.

## 🤝 References

  * Dataset Source: [UDataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS / Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)
  * Inspired by: [Stephan M. Wagner - Bottleneck identification in supply chain networks](https://www.researchgate.net/publication/254305917_Bottleneck_identification_in_supply_chain_networks)

