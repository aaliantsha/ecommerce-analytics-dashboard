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
git clone https://github.com/yourusername/ecommerce-analytics-dashboard.git
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

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - FREE)

This is the easiest and recommended method for hosting your dashboard.

1. **Push your code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/ecommerce-analytics-dashboard.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch (main), and main file (app.py)
   - Click "Deploy"
   - Your app will be live at: `https://yourusername-ecommerce-analytics-dashboard-app-xxxxx.streamlit.app`

3. **Share your link**
   - Copy the URL provided by Streamlit Cloud
   - Add it to your resume, LinkedIn, or portfolio

### Option 2: Heroku (FREE tier available)

1. **Create a Procfile**
```
web: sh setup.sh && streamlit run app.py
```

2. **Create setup.sh**
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. **Deploy to Heroku**
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Render (FREE)

1. Go to [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## 📊 Dashboard Sections

### 1. Key Performance Indicators (KPIs)
- Total Revenue
- Total Transactions
- Total Customers
- Total Products
- Average Order Value

### 2. Revenue Trends
- Monthly revenue line chart
- Sales by day of week bar chart

### 3. Customer Analysis
- Customer segmentation pie chart (Champions, Loyal, At Risk, etc.)
- Top 10 customers by revenue
- RFM analysis metrics (Recency, Frequency, Monetary)

### 4. Product Performance
- Top 15 products by revenue
- Top 15 products by quantity sold

### 5. Geographic Distribution
- Top 10 countries by revenue
- Interactive world map showing sales distribution

### 6. Time-based Patterns
- Hourly sales pattern
- Monthly transaction trends

### 7. Data Explorer
- Filterable raw data table

## 📈 Analytical Insights

### Customer Segmentation (RFM Analysis)
The dashboard implements RFM analysis to segment customers into 7 categories:

1. **Champions** - Recent, frequent, high-value customers (R≥3, F≥3, M≥3)
2. **Loyal Customers** - Regular buyers (R≥3, F≥2)
3. **Big Spenders** - High-value but less frequent (R≥3, M≥3)
4. **Potential Loyalists** - Recent customers with growth potential (R≥2)
5. **At Risk** - Previously frequent buyers showing decline (R=1, F≥3)
6. **Lost Customers** - Haven't purchased recently (R=1)
7. **Others** - Remaining customer segment

### Methodology

**Data Preprocessing:**
1. Remove null CustomerID values
2. Filter out negative quantities (returns)
3. Remove zero/negative unit prices
4. Calculate total price per transaction

**Feature Engineering:**
1. Extract time components (year, month, day, hour)
2. Create month-year periods for trend analysis
3. Calculate total transaction value

**RFM Scoring:**
1. Recency: Days since last purchase
2. Frequency: Number of unique orders
3. Monetary: Total spending
4. Each metric scored 1-4 using quartiles
5. Combined into RFM segments

## 🎓 Skills Demonstrated

### Technical Skills
- ✅ Python programming
- ✅ Data cleaning and preprocessing
- ✅ Feature engineering
- ✅ Exploratory Data Analysis (EDA)
- ✅ Customer segmentation (RFM analysis)
- ✅ Data visualization (Plotly)
- ✅ Web application development (Streamlit)
- ✅ Version control (Git/GitHub)
- ✅ Cloud deployment

### Analytical Skills
- ✅ Business problem identification
- ✅ KPI definition and tracking
- ✅ Trend analysis
- ✅ Customer behavior analysis
- ✅ Product performance analysis
- ✅ Geographic market analysis
- ✅ Time series analysis

### Business Acumen
- ✅ E-commerce domain knowledge
- ✅ Strategic thinking
- ✅ Data-driven decision making
- ✅ Stakeholder communication

## 📝 Project Structure

```
ecommerce-analytics-dashboard/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
└── screenshots/           # Dashboard screenshots (optional)
```

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Your Name**
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [Your GitHub](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Dataset: UCI Machine Learning Repository
- Visualization library: Plotly
- Web framework: Streamlit
- Data analysis: Pandas

## 📞 Contact

For questions or collaboration opportunities, feel free to reach out!

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**
