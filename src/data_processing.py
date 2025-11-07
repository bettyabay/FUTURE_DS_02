"""
Data processing and cleaning functions for social media campaign data
"""

import pandas as pd
import numpy as np
from typing import Optional, List


def load_data(file_path: str, file_type: str = 'csv') -> pd.DataFrame:
    """
    Load data from CSV or Excel file
    
    Parameters:
    -----------
    file_path : str
        Path to the data file
    file_type : str
        Type of file ('csv' or 'excel')
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe
    """
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'excel':
        return pd.read_excel(file_path)
    else:
        raise ValueError("file_type must be 'csv' or 'excel'")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the campaign data
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataframe
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe
    """
    df_clean = df.copy()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Convert date columns if they exist
    date_columns = ['date', 'Date', 'start_date', 'end_date', 'Date start', 'Date stop']
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
    
    # Remove rows with missing critical columns
    # Add your critical columns here based on your data structure
    # df_clean = df_clean.dropna(subset=['critical_column'])
    
    return df_clean


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate campaign performance metrics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned dataframe with campaign data
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with calculated metrics
    """
    df_metrics = df.copy()
    
    # Common column name variations
    impressions_col = _find_column(df_metrics, ['impressions', 'Impressions', 'impression'])
    clicks_col = _find_column(df_metrics, ['clicks', 'Clicks', 'link_clicks', 'Link Clicks'])
    spend_col = _find_column(df_metrics, ['spend', 'Spend', 'amount_spent', 'Amount Spent'])
    reach_col = _find_column(df_metrics, ['reach', 'Reach'])
    engagements_col = _find_column(df_metrics, ['engagements', 'Engagements', 'engagement'])
    conversions_col = _find_column(df_metrics, ['conversions', 'Conversions', 'purchases'])
    revenue_col = _find_column(df_metrics, ['revenue', 'Revenue', 'purchase_value'])
    
    # Calculate CTR (Click-Through Rate)
    if impressions_col and clicks_col:
        df_metrics['CTR'] = (df_metrics[clicks_col] / df_metrics[impressions_col] * 100).fillna(0)
    
    # Calculate CPC (Cost Per Click)
    if spend_col and clicks_col:
        df_metrics['CPC'] = (df_metrics[spend_col] / df_metrics[clicks_col].replace(0, np.nan)).fillna(0)
    
    # Calculate CPM (Cost Per Mille)
    if spend_col and impressions_col:
        df_metrics['CPM'] = (df_metrics[spend_col] / df_metrics[impressions_col] * 1000).fillna(0)
    
    # Calculate Engagement Rate
    if engagements_col and impressions_col:
        df_metrics['Engagement_Rate'] = (df_metrics[engagements_col] / df_metrics[impressions_col] * 100).fillna(0)
    elif engagements_col and reach_col:
        df_metrics['Engagement_Rate'] = (df_metrics[engagements_col] / df_metrics[reach_col] * 100).fillna(0)
    
    # Calculate Conversion Rate
    if conversions_col and clicks_col:
        df_metrics['Conversion_Rate'] = (df_metrics[conversions_col] / df_metrics[clicks_col].replace(0, np.nan) * 100).fillna(0)
    
    # Calculate ROI
    if revenue_col and spend_col:
        df_metrics['ROI'] = ((df_metrics[revenue_col] - df_metrics[spend_col]) / df_metrics[spend_col].replace(0, np.nan) * 100).fillna(0)
    
    # Calculate ROAS (Return on Ad Spend)
    if revenue_col and spend_col:
        df_metrics['ROAS'] = (df_metrics[revenue_col] / df_metrics[spend_col].replace(0, np.nan)).fillna(0)
    
    return df_metrics


def _find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """
    Find a column in dataframe by checking multiple possible names
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to search
    possible_names : List[str]
        List of possible column names
    
    Returns:
    --------
    Optional[str]
        Found column name or None
    """
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def prepare_dashboard_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare data specifically for dashboard visualization
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with metrics
    
    Returns:
    --------
    pd.DataFrame
        Dataframe ready for dashboard
    """
    df_dashboard = df.copy()
    
    # Add date columns for time series analysis
    date_col = _find_column(df_dashboard, ['date', 'Date', 'start_date', 'Date start'])
    if date_col:
        df_dashboard['Year'] = pd.to_datetime(df_dashboard[date_col]).dt.year
        df_dashboard['Month'] = pd.to_datetime(df_dashboard[date_col]).dt.month
        df_dashboard['Week'] = pd.to_datetime(df_dashboard[date_col]).dt.isocalendar().week
        df_dashboard['Day'] = pd.to_datetime(df_dashboard[date_col]).dt.day
    
    return df_dashboard

