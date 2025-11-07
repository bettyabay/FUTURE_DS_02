"""
Social Media Campaign Performance Tracker - Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add src to path
sys.path.append('../src')
from data_processing import load_data
from analysis import get_campaign_summary, get_top_performing_ads, get_campaign_performance_by_dimension
from utils import format_currency, format_percentage

# Page configuration
st.set_page_config(
    page_title="Social Media Campaign Performance Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Social Media Campaign Performance Tracker</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Overview", "Campaign Analysis", "Performance Metrics", "Top Performers", "Recommendations"]
)

# Load data
@st.cache_data
def load_campaign_data():
    """Load campaign data with caching"""
    data_path = '../data/processed/dashboard_data.csv'
    if os.path.exists(data_path):
        return load_data(data_path, file_type='csv')
    else:
        # Try cleaned data as fallback
        data_path = '../data/processed/cleaned_campaign_data.csv'
        if os.path.exists(data_path):
            return load_data(data_path, file_type='csv')
        else:
            st.error("Data file not found! Please run the data preparation notebooks first.")
            return None

df = load_campaign_data()

if df is not None:
    # Overview Page
    if page == "Overview":
        st.header("Campaign Overview")
        
        # Get summary statistics
        summary = get_campaign_summary(df)
        
        # Display KPI cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'Total_Spend' in summary:
                st.metric("Total Spend", format_currency(summary['Total_Spend']))
            else:
                st.metric("Total Spend", "N/A")
        
        with col2:
            if 'Total_Impressions' in summary:
                st.metric("Total Impressions", f"{summary['Total_Impressions']:,.0f}")
            else:
                st.metric("Total Impressions", "N/A")
        
        with col3:
            if 'Avg_CTR' in summary:
                st.metric("Average CTR", format_percentage(summary['Avg_CTR']))
            else:
                st.metric("Average CTR", "N/A")
        
        with col4:
            if 'Avg_ROI' in summary:
                st.metric("Average ROI", format_percentage(summary['Avg_ROI']))
            else:
                st.metric("Average ROI", "N/A")
        
        # Campaign overview chart
        st.subheader("Campaign Performance Overview")
        
        # Create overview visualization
        if 'CTR' in df.columns and 'ROI' in df.columns:
            fig = px.scatter(
                df, 
                x='CTR', 
                y='ROI',
                size='Spend' if 'Spend' in df.columns else None,
                hover_data=df.columns.tolist(),
                title='CTR vs ROI Performance'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Campaign Analysis Page
    elif page == "Campaign Analysis":
        st.header("Campaign Analysis")
        
        # Filters
        st.sidebar.subheader("Filters")
        
        # Date filter
        date_col = None
        for col in ['date', 'Date', 'start_date', 'Date start']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            min_date = df[date_col].min().date() if pd.notna(df[date_col].min()) else None
            max_date = df[date_col].max().date() if pd.notna(df[date_col].max()) else None
            if min_date and max_date:
                date_range = st.sidebar.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                # Filter data by date range if both dates selected
                if isinstance(date_range, tuple) and len(date_range) == 2:
                    mask = (df[date_col].dt.date >= date_range[0]) & (df[date_col].dt.date <= date_range[1])
                    df = df[mask]
        
        # Dimension selector
        dimension_options = []
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].nunique() < 20:
                dimension_options.append(col)
        
        selected_dimension = st.sidebar.selectbox("Group By", dimension_options)
        
        # Performance by dimension
        if selected_dimension:
            st.subheader(f"Performance by {selected_dimension}")
            perf_by_dim = get_campaign_performance_by_dimension(df, selected_dimension)
            st.dataframe(perf_by_dim)
            
            # Visualization
            if 'ROI' in perf_by_dim.columns:
                fig = px.bar(
                    perf_by_dim.head(10),
                    x=selected_dimension,
                    y='ROI',
                    title=f'Average ROI by {selected_dimension}'
                )
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
    
    # Performance Metrics Page
    elif page == "Performance Metrics":
        st.header("Performance Metrics")
        
        # Metric selector
        metric_options = [col for col in df.columns if col in ['CTR', 'CPC', 'CPM', 'Engagement_Rate', 'Conversion_Rate', 'ROI', 'ROAS']]
        selected_metric = st.selectbox("Select Metric", metric_options)
        
        if selected_metric:
            # Distribution
            st.subheader(f"{selected_metric} Distribution")
            fig = px.histogram(df, x=selected_metric, nbins=30, title=f'Distribution of {selected_metric}')
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean", f"{df[selected_metric].mean():.2f}")
            with col2:
                st.metric("Median", f"{df[selected_metric].median():.2f}")
            with col3:
                st.metric("Std Dev", f"{df[selected_metric].std():.2f}")
    
    # Top Performers Page
    elif page == "Top Performers":
        st.header("Top Performers")
        
        # Metric selector
        metric_options = [col for col in df.columns if col in ['CTR', 'CPC', 'CPM', 'Engagement_Rate', 'Conversion_Rate', 'ROI', 'ROAS']]
        selected_metric = st.selectbox("Rank By", metric_options)
        n_top = st.slider("Number of Top Performers", 5, 20, 10)
        
        if selected_metric:
            top_performers = get_top_performing_ads(df, metric=selected_metric, n=n_top)
            st.dataframe(top_performers)
            
            # Visualization
            id_col = None
            for col in ['campaign', 'Campaign', 'ad_name', 'ad_id', 'Ad name']:
                if col in top_performers.columns:
                    id_col = col
                    break
            
            if id_col:
                fig = px.bar(
                    top_performers,
                    x=id_col,
                    y=selected_metric,
                    title=f'Top {n_top} Performers by {selected_metric}'
                )
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations Page
    elif page == "Recommendations":
        st.header("Actionable Recommendations")
        
        # Generate recommendations based on data
        recommendations = []
        
        if 'CTR' in df.columns:
            avg_ctr = df['CTR'].mean()
            if avg_ctr < 2.0:
                recommendations.append("⚠️ **Low CTR**: Consider improving ad creatives and targeting to increase click-through rates.")
            elif avg_ctr > 5.0:
                recommendations.append("✅ **Good CTR**: Maintain current creative strategy.")
        
        if 'ROI' in df.columns:
            avg_roi = df['ROI'].mean()
            if avg_roi < 0:
                recommendations.append("⚠️ **Negative ROI**: Review campaign strategy and consider pausing underperforming campaigns.")
            elif avg_roi > 100:
                recommendations.append("✅ **Excellent ROI**: Consider scaling successful campaigns.")
        
        if 'CPC' in df.columns:
            avg_cpc = df['CPC'].mean()
            recommendations.append(f"💰 **Average CPC**: ${avg_cpc:.2f}. Monitor and optimize bids to reduce costs.")
        
        # Display recommendations
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Additional insights
        st.subheader("Key Insights")
        
        if 'campaign' in df.columns or 'Campaign' in df.columns:
            campaign_col = 'campaign' if 'campaign' in df.columns else 'Campaign'
            if 'ROI' in df.columns:
                best_campaign = df.groupby(campaign_col)['ROI'].mean().idxmax()
                st.info(f"🏆 **Best Performing Campaign**: {best_campaign}")

else:
    st.warning("""
    ## Data Not Found
    
    Please follow these steps:
    1. Place your raw data file in `data/raw/` directory
    2. Run the notebooks in order:
       - `01_data_exploration.ipynb`
       - `02_data_cleaning.ipynb`
       - `03_analysis.ipynb`
       - `04_visualizations.ipynb`
       - `05_dashboard_prep.ipynb`
    3. Reload this dashboard
    """)

