"""
Visualization functions for campaign performance data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, List


def set_style():
    """Set matplotlib and seaborn style"""
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except:
        try:
            plt.style.use('seaborn-darkgrid')
        except:
            plt.style.use('ggplot')
    sns.set_palette("husl")


def plot_ctr_over_time(df: pd.DataFrame, date_column: Optional[str] = None, 
                       save_path: Optional[str] = None):
    """
    Plot CTR over time
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with time series data
    date_column : Optional[str]
        Name of date column
    save_path : Optional[str]
        Path to save the figure
    """
    if date_column is None:
        date_column = _find_column(df, ['date', 'Date', 'start_date'])
    
    if date_column is None or 'CTR' not in df.columns:
        print("Required columns not found")
        return
    
    fig = px.line(df, x=date_column, y='CTR', 
                  title='Click-Through Rate (CTR) Over Time',
                  labels={'CTR': 'CTR (%)', date_column: 'Date'})
    fig.update_layout(template='plotly_white')
    fig.show()
    
    if save_path:
        fig.write_image(save_path)


def plot_roi_comparison(df: pd.DataFrame, group_by: str, 
                        save_path: Optional[str] = None):
    """
    Plot ROI comparison across different groups
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    group_by : str
        Column to group by (e.g., 'campaign_name', 'age', 'device')
    save_path : Optional[str]
        Path to save the figure
    """
    if 'ROI' not in df.columns or group_by not in df.columns:
        print("Required columns not found")
        return
    
    grouped = df.groupby(group_by)['ROI'].mean().sort_values(ascending=False)
    
    fig = px.bar(x=grouped.index, y=grouped.values,
                 title=f'Average ROI by {group_by}',
                 labels={'x': group_by, 'y': 'ROI (%)'})
    fig.update_layout(template='plotly_white', xaxis_tickangle=-45)
    fig.show()
    
    if save_path:
        fig.write_image(save_path)


def plot_metric_distribution(df: pd.DataFrame, metric: str, 
                            save_path: Optional[str] = None):
    """
    Plot distribution of a metric
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    metric : str
        Metric to plot (e.g., 'CTR', 'CPC', 'ROI')
    save_path : Optional[str]
        Path to save the figure
    """
    if metric not in df.columns:
        print(f"Metric '{metric}' not found in dataframe")
        return
    
    fig = px.histogram(df, x=metric, nbins=30,
                      title=f'Distribution of {metric}',
                      labels={metric: metric})
    fig.update_layout(template='plotly_white')
    fig.show()
    
    if save_path:
        fig.write_image(save_path)


def plot_campaign_overview(df: pd.DataFrame, save_path: Optional[str] = None):
    """
    Create a comprehensive campaign overview dashboard
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    save_path : Optional[str]
        Path to save the figure
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CTR Distribution', 'ROI by Campaign', 
                       'Spend vs Revenue', 'Engagement Rate'),
        specs=[[{"type": "histogram"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "box"}]]
    )
    
    # CTR Distribution
    if 'CTR' in df.columns:
        fig.add_trace(
            go.Histogram(x=df['CTR'], name='CTR'),
            row=1, col=1
        )
    
    # ROI by Campaign (if campaign column exists)
    campaign_col = _find_column(df, ['campaign', 'Campaign', 'campaign_name'])
    if 'ROI' in df.columns and campaign_col:
        roi_by_campaign = df.groupby(campaign_col)['ROI'].mean().sort_values(ascending=False).head(10)
        fig.add_trace(
            go.Bar(x=roi_by_campaign.index, y=roi_by_campaign.values, name='ROI'),
            row=1, col=2
        )
    
    # Spend vs Revenue
    spend_col = _find_column(df, ['spend', 'Spend'])
    revenue_col = _find_column(df, ['revenue', 'Revenue'])
    if spend_col and revenue_col:
        fig.add_trace(
            go.Scatter(x=df[spend_col], y=df[revenue_col], mode='markers', name='Spend vs Revenue'),
            row=2, col=1
        )
    
    # Engagement Rate
    if 'Engagement_Rate' in df.columns:
        fig.add_trace(
            go.Box(y=df['Engagement_Rate'], name='Engagement Rate'),
            row=2, col=2
        )
    
    fig.update_layout(height=800, title_text="Campaign Performance Overview", 
                     template='plotly_white', showlegend=False)
    fig.show()
    
    if save_path:
        fig.write_image(save_path)


def plot_top_performers(df: pd.DataFrame, metric: str = 'CTR', n: int = 10,
                       save_path: Optional[str] = None):
    """
    Plot top performing campaigns/ads
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    metric : str
        Metric to rank by
    n : int
        Number of top performers to show
    save_path : Optional[str]
        Path to save the figure
    """
    if metric not in df.columns:
        print(f"Metric '{metric}' not found")
        return
    
    # Get identifier column
    id_col = _find_column(df, ['campaign', 'Campaign', 'ad_name', 'ad_id', 'Ad name'])
    if id_col is None:
        id_col = df.index.name or 'Index'
        df_plot = df.nlargest(n, metric).reset_index()
    else:
        df_plot = df.nlargest(n, metric)
    
    fig = px.bar(df_plot, x=id_col, y=metric,
                title=f'Top {n} Performers by {metric}',
                labels={id_col: 'Campaign/Ad', metric: metric})
    fig.update_layout(template='plotly_white', xaxis_tickangle=-45)
    fig.show()
    
    if save_path:
        fig.write_image(save_path)


def _find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """Helper function to find column by multiple possible names"""
    for name in possible_names:
        if name in df.columns:
            return name
    return None

