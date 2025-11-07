"""
Analysis functions for campaign performance evaluation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def get_campaign_summary(df: pd.DataFrame) -> Dict:
    """
    Get overall campaign summary statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data and metrics
    
    Returns:
    --------
    Dict
        Dictionary with summary statistics
    """
    summary = {}
    
    # Find relevant columns
    spend_col = _find_column(df, ['spend', 'Spend', 'amount_spent', 'Amount Spent'])
    impressions_col = _find_column(df, ['impressions', 'Impressions'])
    clicks_col = _find_column(df, ['clicks', 'Clicks', 'link_clicks'])
    revenue_col = _find_column(df, ['revenue', 'Revenue', 'purchase_value'])
    
    if spend_col:
        summary['Total_Spend'] = df[spend_col].sum()
        summary['Avg_Spend'] = df[spend_col].mean()
    
    if impressions_col:
        summary['Total_Impressions'] = df[impressions_col].sum()
        summary['Avg_Impressions'] = df[impressions_col].mean()
    
    if clicks_col:
        summary['Total_Clicks'] = df[clicks_col].sum()
        summary['Avg_Clicks'] = df[clicks_col].mean()
    
    if 'CTR' in df.columns:
        summary['Avg_CTR'] = df['CTR'].mean()
    
    if 'CPC' in df.columns:
        summary['Avg_CPC'] = df['CPC'].mean()
    
    if 'ROI' in df.columns:
        summary['Avg_ROI'] = df['ROI'].mean()
        summary['Total_ROI'] = df['ROI'].sum()
    
    if revenue_col:
        summary['Total_Revenue'] = df[revenue_col].sum()
    
    if 'ROAS' in df.columns:
        summary['Avg_ROAS'] = df['ROAS'].mean()
    
    return summary


def get_top_performing_ads(df: pd.DataFrame, metric: str = 'CTR', n: int = 10) -> pd.DataFrame:
    """
    Get top performing ads based on a metric
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    metric : str
        Metric to rank by (default: 'CTR')
    n : int
        Number of top ads to return (default: 10)
    
    Returns:
    --------
    pd.DataFrame
        Top n performing ads
    """
    if metric not in df.columns:
        raise ValueError(f"Metric '{metric}' not found in dataframe")
    
    top_ads = df.nlargest(n, metric)
    return top_ads


def get_campaign_performance_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """
    Get performance metrics grouped by a dimension (e.g., campaign, age, region, device)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    dimension : str
        Column name to group by
    
    Returns:
    --------
    pd.DataFrame
        Aggregated performance by dimension
    """
    if dimension not in df.columns:
        raise ValueError(f"Dimension '{dimension}' not found in dataframe")
    
    # Find metric columns
    metric_cols = ['CTR', 'CPC', 'CPM', 'Engagement_Rate', 'Conversion_Rate', 'ROI', 'ROAS']
    available_metrics = [col for col in metric_cols if col in df.columns]
    
    # Find spending columns
    spend_col = _find_column(df, ['spend', 'Spend', 'amount_spent'])
    impressions_col = _find_column(df, ['impressions', 'Impressions'])
    clicks_col = _find_column(df, ['clicks', 'Clicks'])
    
    agg_dict = {}
    if spend_col:
        agg_dict[spend_col] = 'sum'
    if impressions_col:
        agg_dict[impressions_col] = 'sum'
    if clicks_col:
        agg_dict[clicks_col] = 'sum'
    
    for metric in available_metrics:
        agg_dict[metric] = 'mean'
    
    grouped = df.groupby(dimension).agg(agg_dict).reset_index()
    
    return grouped


def get_time_series_data(df: pd.DataFrame, date_column: Optional[str] = None) -> pd.DataFrame:
    """
    Aggregate data by time period for time series analysis
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with campaign data
    date_column : Optional[str]
        Name of date column (auto-detected if None)
    
    Returns:
    --------
    pd.DataFrame
        Time series aggregated data
    """
    if date_column is None:
        date_column = _find_column(df, ['date', 'Date', 'start_date', 'Date start'])
    
    if date_column is None:
        raise ValueError("No date column found in dataframe")
    
    df_time = df.copy()
    df_time[date_column] = pd.to_datetime(df_time[date_column])
    df_time = df_time.set_index(date_column)
    
    # Aggregate by date
    spend_col = _find_column(df_time, ['spend', 'Spend'])
    impressions_col = _find_column(df_time, ['impressions', 'Impressions'])
    clicks_col = _find_column(df_time, ['clicks', 'Clicks'])
    
    agg_dict = {}
    if spend_col:
        agg_dict[spend_col] = 'sum'
    if impressions_col:
        agg_dict[impressions_col] = 'sum'
    if clicks_col:
        agg_dict[clicks_col] = 'sum'
    
    df_daily = df_time.resample('D').agg(agg_dict)
    
    # Recalculate metrics
    if spend_col and clicks_col:
        df_daily['CTR'] = (df_daily[clicks_col] / df_daily[impressions_col] * 100).fillna(0)
        df_daily['CPC'] = (df_daily[spend_col] / df_daily[clicks_col].replace(0, np.nan)).fillna(0)
    
    return df_daily.reset_index()


def _find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """Helper function to find column by multiple possible names"""
    for name in possible_names:
        if name in df.columns:
            return name
    return None

