# 🛒 E-Commerce Sales Analytics Dashboard

A comprehensive, interactive analytics dashboard built with Python and Streamlit for analyzing e-commerce sales data. This project demonstrates end-to-end data analysis capabilities including data cleaning, feature engineering, customer segmentation, and interactive visualizations.

## 📊 Project Overview

### Problem Statement
E-commerce businesses need to understand their sales performance, customer behavior, and product trends to make informed, data-driven decisions that drive growth and profitability.

### Objectives
1. **Revenue Analysis** - Track and analyze revenue trends over time to identify growth patterns
2. **Customer Segmentation** - Implement RFM (Recency, Frequency, Monetary) analysis to categorize customers
3. **Product Performance** - Identify top-performing products and optimize inventory
4. **Geographic Analysis** - Understand sales distribution across different markets
5. **Time-based Patterns** - Discover peak sales periods and seasonal trends

### Key Business Questions Answered
- What are the overall sales trends and revenue patterns?
- Who are our most valuable customers and how should we segment them?
- Which products drive the most revenue and quantity sold?
- When do customers prefer to shop (day, hour, month)?
- Which geographic markets should we prioritize?

## 🎯 Features

- **Interactive Dashboard**: Real-time filtering by date range and country
- **KPI Metrics**: Total revenue, transactions, customers, products, and average order value
- **Revenue Trends**: Monthly trends and day-of-week analysis
- **Customer Segmentation**: RFM analysis with 7 customer segments
- **Product Analysis**: Top performers by revenue and quantity
- **Geographic Insights**: Country-wise revenue distribution with interactive maps
- **Time Patterns**: Hourly and monthly sales patterns
- **Raw Data Explorer**: Browse and filter the underlying dataset

## 📁 Dataset

**Source**: [UCI Machine Learning Repository - Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail)

**Description**: 
- Transnational data set containing all transactions occurring between 01/12/2010 and 09/12/2011
- UK-based online retail company specializing in gifts and homewares
- 541,909 transactions from 4,372 customers across 38 countries
- 8 features including InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, and Country

**Data Quality**:
- Removed transactions with missing CustomerID
- Filtered out negative quantities (returns) and zero prices
- Created derived features for time-based analysis

## 🛠️ Technical Stack

- **Python 3.8+**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations
- **Openpyxl** - Excel file handling

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/aaliantsha/ecommerce-analytics-dashboard.git
cd ecommerce-analytics-dashboard
```

2. **Create a virtual environment (recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the dashboard**
- Open your browser and go to `http://localhost:8501`
- The dashboard will automatically load and fetch the dataset