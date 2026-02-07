import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-Commerce Sales Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the Online Retail dataset"""
    try:
        # Load data from UCI repository
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
        df = pd.read_excel(url)
        
        # Data cleaning
        df = df.dropna(subset=['CustomerID'])
        df['CustomerID'] = df['CustomerID'].astype(int)
        df = df[df['Quantity'] > 0]
        df = df[df['UnitPrice'] > 0]
        
        # Feature engineering
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        df['Year'] = df['InvoiceDate'].dt.year
        df['Month'] = df['InvoiceDate'].dt.month
        df['MonthYear'] = df['InvoiceDate'].dt.to_period('M').astype(str)
        df['Day'] = df['InvoiceDate'].dt.day_name()
        df['Hour'] = df['InvoiceDate'].dt.hour
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def calculate_kpis(df):
    """Calculate key performance indicators"""
    total_revenue = df['TotalPrice'].sum()
    total_transactions = df['InvoiceNo'].nunique()
    total_customers = df['CustomerID'].nunique()
    total_products = df['StockCode'].nunique()
    avg_order_value = total_revenue / total_transactions
    
    return {
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'total_customers': total_customers,
        'total_products': total_products,
        'avg_order_value': avg_order_value
    }

def customer_segmentation(df):
    """Perform RFM (Recency, Frequency, Monetary) analysis safely."""
    snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)
    
    # Aggregate RFM values
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    }).reset_index()
    
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    # Safe qcut function
    def safe_qcut(series, q=4, ascending=True):
        try:
            # Determine number of unique bins
            bins = min(q, series.nunique())
            # Generate labels dynamically
            labels = list(range(bins, 0, -1)) if ascending else list(range(1, bins + 1))
            return pd.qcut(series, bins, labels=labels, duplicates='drop')
        except ValueError:
            # If all values identical, assign middle score
            return pd.Series([q // 2] * len(series), index=series.index)
    
    # Create RFM scores safely
    rfm['R_Score'] = safe_qcut(rfm['Recency'], q=4, ascending=False)
    rfm['F_Score'] = safe_qcut(rfm['Frequency'], q=4, ascending=True)
    rfm['M_Score'] = safe_qcut(rfm['Monetary'], q=4, ascending=True)
    
    # Combine RFM score
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

    # Segment customers
    def segment_customers(row):
        if row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
            return 'Champions'
        elif row['R_Score'] >= 3 and row['F_Score'] >= 2:
            return 'Loyal Customers'
        elif row['R_Score'] >= 3 and row['M_Score'] >= 3:
            return 'Big Spenders'
        elif row['R_Score'] >= 2:
            return 'Potential Loyalists'
        elif row['R_Score'] == 1 and row['F_Score'] >= 3:
            return 'At Risk'
        elif row['R_Score'] == 1:
            return 'Lost Customers'
        else:
            return 'Others'
    
    rfm['Segment'] = rfm.apply(segment_customers, axis=1)
    
    return rfm

def main():
    # Header
    st.title("🛒 E-Commerce Sales Analytics Dashboard")
    st.markdown("**Comprehensive analysis of online retail transactions**")
    st.markdown("---")
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['InvoiceDate'].min().date()
    max_date = df['InvoiceDate'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Country filter
    countries = ['All'] + sorted(df['Country'].unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", countries)
    
    # Apply filters
    if len(date_range) == 2:
        df_filtered = df[
            (df['InvoiceDate'].dt.date >= date_range[0]) &
            (df['InvoiceDate'].dt.date <= date_range[1])
        ]
    else:
        df_filtered = df.copy()
    
    if selected_country != 'All':
        df_filtered = df_filtered[df_filtered['Country'] == selected_country]
    
    # Problem Statement Section
    with st.expander("📋 **Problem Statement & Objectives**", expanded=False):
        st.markdown("""
        ### Problem Statement
        The e-commerce company needs to understand its sales performance, customer behavior, 
        and product trends to make data-driven decisions for business growth.
        
        ### Objectives
        1. **Revenue Analysis**: Track and analyze revenue trends over time
        2. **Customer Segmentation**: Identify and categorize customers based on purchasing behavior
        3. **Product Performance**: Determine top-performing products and categories
        4. **Geographic Analysis**: Understand sales distribution across different countries
        5. **Time-based Patterns**: Identify peak sales periods and seasonal trends
        
        ### Key Questions
        - What are the overall sales trends?
        - Who are our most valuable customers?
        - Which products drive the most revenue?
        - When do customers prefer to shop?
        - Which markets should we focus on?
        """)
    
    # Calculate KPIs
    kpis = calculate_kpis(df_filtered)
    
    # Display KPIs
    st.header("📊 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${kpis['total_revenue']:,.2f}",
            delta="Revenue Generated"
        )
    
    with col2:
        st.metric(
            label="Total Transactions",
            value=f"{kpis['total_transactions']:,}",
            delta="Unique Orders"
        )
    
    with col3:
        st.metric(
            label="Total Customers",
            value=f"{kpis['total_customers']:,}",
            delta="Unique Customers"
        )
    
    with col4:
        st.metric(
            label="Total Products",
            value=f"{kpis['total_products']:,}",
            delta="Unique Items"
        )
    
    with col5:
        st.metric(
            label="Avg Order Value",
            value=f"${kpis['avg_order_value']:,.2f}",
            delta="Per Transaction"
        )
    
    st.markdown("---")
    
    # Revenue Trends
    st.header("📈 Revenue Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly revenue trend
        monthly_revenue = df_filtered.groupby('MonthYear')['TotalPrice'].sum().reset_index()
        monthly_revenue = monthly_revenue.sort_values('MonthYear')
        
        fig_monthly = px.line(
            monthly_revenue,
            x='MonthYear',
            y='TotalPrice',
            title='Monthly Revenue Trend',
            labels={'TotalPrice': 'Revenue ($)', 'MonthYear': 'Month-Year'}
        )
        fig_monthly.update_traces(line_color='#1f77b4', line_width=3)
        fig_monthly.update_layout(hovermode='x unified')
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col2:
        # Daily sales pattern
        daily_sales = df_filtered.groupby('Day')['TotalPrice'].sum().reset_index()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_sales['Day'] = pd.Categorical(daily_sales['Day'], categories=day_order, ordered=True)
        daily_sales = daily_sales.sort_values('Day')
        
        fig_daily = px.bar(
            daily_sales,
            x='Day',
            y='TotalPrice',
            title='Sales by Day of Week',
            labels={'TotalPrice': 'Revenue ($)', 'Day': 'Day of Week'},
            color='TotalPrice',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_daily, use_container_width=True)
    
    st.markdown("---")
    
    # Customer Analysis
    st.header("👥 Customer Analysis")
    
    # Perform RFM analysis
    rfm = customer_segmentation(df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer segments
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        fig_segments = px.pie(
            segment_counts,
            values='Count',
            names='Segment',
            title='Customer Segmentation',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_segments, use_container_width=True)
    
    with col2:
        # Top 10 customers by revenue
        top_customers = df_filtered.groupby('CustomerID')['TotalPrice'].sum().reset_index()
        top_customers = top_customers.sort_values('TotalPrice', ascending=False).head(10)
        top_customers['CustomerID'] = top_customers['CustomerID'].astype(str)
        
        fig_top_customers = px.bar(
            top_customers,
            x='TotalPrice',
            y='CustomerID',
            title='Top 10 Customers by Revenue',
            labels={'TotalPrice': 'Revenue ($)', 'CustomerID': 'Customer ID'},
            orientation='h',
            color='TotalPrice',
            color_continuous_scale='Viridis'
        )
        # fig_top_customers.update_xaxes(
        #     tickformat=",d",
        #     exponentformat="none"
        # )

        fig_top_customers.update_traces(
            hovertemplate=
            "Customer ID: %{y}<br>" +
            "Revenue: %{x:,.0f}<extra></extra>"
            )
        st.plotly_chart(fig_top_customers, use_container_width=True)
    
    # RFM metrics
    st.subheader("RFM Analysis Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Recency (days)", f"{rfm['Recency'].mean():.0f}")
    with col2:
        st.metric("Avg Frequency", f"{rfm['Frequency'].mean():.1f}")
    with col3:
        st.metric("Avg Monetary ($)", f"${rfm['Monetary'].mean():,.2f}")
    
    st.markdown("---")
    
    # Product Analysis
    st.header("🏆 Product Performance")
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 15 products by revenue
        top_products = df_filtered.groupby('Description')['TotalPrice'].sum().reset_index()
        top_products = top_products.sort_values('TotalPrice', ascending=False).head(15)
        
        fig_products = px.bar(
            top_products,
            x='TotalPrice',
            y='Description',
            title='Top 15 Products by Revenue',
            labels={'TotalPrice': 'Revenue ($)', 'Description': 'Product'},
            orientation='h',
            color='TotalPrice',
            color_continuous_scale='Oranges'
        )
        fig_products.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col2:
        # Top 15 products by quantity sold
        top_qty = df_filtered.groupby('Description')['Quantity'].sum().reset_index()
        top_qty = top_qty.sort_values('Quantity', ascending=False).head(15)
        
        fig_qty = px.bar(
            top_qty,
            x='Quantity',
            y='Description',
            title='Top 15 Products by Quantity Sold',
            labels={'Quantity': 'Quantity Sold', 'Description': 'Product'},
            orientation='h',
            color='Quantity',
            color_continuous_scale='Greens'
        )
        fig_qty.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_qty, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic Analysis
    st.header("🌍 Geographic Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 countries by revenue
        country_revenue = df_filtered.groupby('Country')['TotalPrice'].sum().reset_index()
        country_revenue = country_revenue.sort_values('TotalPrice', ascending=False).head(10)
        
        fig_countries = px.bar(
            country_revenue,
            x='Country',
            y='TotalPrice',
            title='Top 10 Countries by Revenue',
            labels={'TotalPrice': 'Revenue ($)', 'Country': 'Country'},
            color='TotalPrice',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_countries, use_container_width=True)
    
    with col2:
        # Revenue distribution by country (map)
        country_data = df_filtered.groupby('Country').agg({
            'TotalPrice': 'sum',
            'InvoiceNo': 'nunique'
        }).reset_index()
        country_data.columns = ['Country', 'Revenue', 'Transactions']
        
        fig_map = px.scatter_geo(
            country_data,
            locations='Country',
            locationmode='country names',
            size='Revenue',
            hover_name='Country',
            hover_data={'Revenue': ':,.2f', 'Transactions': ':,'},
            title='Global Sales Distribution',
            color='Revenue',
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # Time-based Analysis
    st.header("⏰ Time-based Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly sales pattern
        hourly_sales = df_filtered.groupby('Hour')['TotalPrice'].sum().reset_index()
        
        fig_hourly = px.line(
            hourly_sales,
            x='Hour',
            y='TotalPrice',
            title='Sales by Hour of Day',
            labels={'TotalPrice': 'Revenue ($)', 'Hour': 'Hour of Day'},
            markers=True
        )
        fig_hourly.update_traces(line_color='#ff7f0e', line_width=3)
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        # Monthly transaction count
        monthly_transactions = df_filtered.groupby('MonthYear')['InvoiceNo'].nunique().reset_index()
        monthly_transactions = monthly_transactions.sort_values('MonthYear')
        
        fig_trans = px.area(
            monthly_transactions,
            x='MonthYear',
            y='InvoiceNo',
            title='Monthly Transaction Count',
            labels={'InvoiceNo': 'Number of Transactions', 'MonthYear': 'Month-Year'}
        )
        fig_trans.update_traces(fillcolor='rgba(31, 119, 180, 0.3)', line_color='#1f77b4')
        st.plotly_chart(fig_trans, use_container_width=True)
    
    st.markdown("---")
    
    # Data Table
    st.header("📋 Raw Data Sample")
    st.dataframe(
        df_filtered.head(100)[['InvoiceNo', 'InvoiceDate', 'Description', 'Quantity', 
                                'UnitPrice', 'TotalPrice', 'CustomerID', 'Country']],
        use_container_width=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p><strong>E-Commerce Sales Analytics Dashboard</strong></p>
        <p>Built with Streamlit & Plotly | Data Source: UCI Machine Learning Repository</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
