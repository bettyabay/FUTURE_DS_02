"""
Data processing and cleaning functions for social media campaign data
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any


DEFAULT_DATE_COLUMNS = [
    'reporting_start',
    'reporting_end',
    'date',
    'Date',
    'start_date',
    'end_date',
    'Date start',
    'Date stop'
]

IDENTIFIER_COLUMNS = [
    'ad_id',
    'campaign_id',
    'fb_campaign_id'
]

NUMERIC_COLUMNS = [
    'impressions',
    'clicks',
    'spent',
    'total_conversion',
    'approved_conversion'
]


def load_data(
    file_path: str,
    file_type: str = 'csv',
    parse_dates: Optional[List[str]] = None,
    enforce_dtypes: bool = True
) -> pd.DataFrame:
    """
    Load data from CSV or Excel file
    
    Parameters:
    -----------
    file_path : str
        Path to the data file
    file_type : str
        Type of file ('csv' or 'excel')
    parse_dates : Optional[List[str]]
        Explicit list of date columns to parse. Defaults to common campaign date columns.
    enforce_dtypes : bool
        Whether to coerce numeric/id columns to consistent dtypes after loading.
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe
    """
    parse_dates = parse_dates or DEFAULT_DATE_COLUMNS
    df: pd.DataFrame

    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type == 'excel':
        df = pd.read_excel(file_path)
    else:
        raise ValueError("file_type must be 'csv' or 'excel'")

    if enforce_dtypes:
        df = _coerce_schema(df, parse_dates=parse_dates)

    return df


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

    # Standardise column names (lower snake_case for consistency)
    df_clean.columns = [col.strip() for col in df_clean.columns]

    # Convert date columns
    for col in DEFAULT_DATE_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(
                df_clean[col],
                errors='coerce',
                dayfirst=True
            )

    # Convert numeric columns
    for col in NUMERIC_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # Remove rows with no impressions or clicks when spend exists
    if 'impressions' in df_clean.columns:
        df_clean = df_clean[df_clean['impressions'].fillna(0) >= 0]
    if 'spent' in df_clean.columns:
        df_clean = df_clean[df_clean['spent'].fillna(0) >= 0]

    # Drop rows missing essential identifiers
    critical_cols = [col for col in IDENTIFIER_COLUMNS if col in df_clean.columns]
    if critical_cols:
        df_clean = df_clean.dropna(subset=critical_cols, how='all')

    # Reset index after cleaning
    df_clean = df_clean.reset_index(drop=True)
    
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
    spend_col = _find_column(df_metrics, ['spent', 'spend', 'Spend', 'amount_spent', 'Amount Spent'])
    total_conv_col = _find_column(df_metrics, ['total_conversion', 'total_conversions', 'conversions', 'Conversions'])
    approved_conv_col = _find_column(df_metrics, ['approved_conversion', 'approved_conversions'])
    reach_col = _find_column(df_metrics, ['reach', 'Reach'])
    engagements_col = _find_column(df_metrics, ['engagements', 'Engagements', 'engagement'])
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
    
    # Calculate Conversion Rate (total conversions / clicks)
    if total_conv_col and clicks_col:
        df_metrics['Conversion_Rate'] = (
            df_metrics[total_conv_col] / df_metrics[clicks_col].replace(0, np.nan) * 100
        ).fillna(0)

    # Calculate Cost Per Acquisition (CPA) variants
    if total_conv_col and spend_col:
        df_metrics['CPA_Total'] = (
            df_metrics[spend_col] / df_metrics[total_conv_col].replace(0, np.nan)
        ).fillna(0)
    if approved_conv_col and spend_col:
        df_metrics['CPA_Approved'] = (
            df_metrics[spend_col] / df_metrics[approved_conv_col].replace(0, np.nan)
        ).fillna(0)

    # Approval rate between total and approved conversions
    if total_conv_col and approved_conv_col:
        df_metrics['Approval_Rate'] = (
            df_metrics[approved_conv_col] / df_metrics[total_conv_col].replace(0, np.nan) * 100
        ).fillna(0)
    
    # Calculate ROI
    if revenue_col and spend_col:
        df_metrics['ROI'] = (
            (df_metrics[revenue_col] - df_metrics[spend_col]) /
            df_metrics[spend_col].replace(0, np.nan) * 100
        ).fillna(0)
        df_metrics['ROAS'] = (
            df_metrics[revenue_col] / df_metrics[spend_col].replace(0, np.nan)
        ).fillna(0)
    elif approved_conv_col and spend_col:
        # Use approved conversions as a lightweight revenue proxy when actual revenue is absent
        df_metrics['ROAS'] = (
            df_metrics[approved_conv_col] / df_metrics[spend_col].replace(0, np.nan)
        ).fillna(0)
    
    return df_metrics


def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate lightweight data-quality diagnostics for the campaign dataset.

    Returns a dictionary with summary tables that can be easily displayed in notebooks.
    """
    summary_rows = [
        ('rows', len(df)),
        ('columns', df.shape[1]),
        ('duplicate_rows', int(df.duplicated().sum()))
    ]

    if 'impressions' in df.columns:
        summary_rows.append(('zero_impressions_rows', int((df['impressions'] == 0).sum())))
    if 'clicks' in df.columns:
        summary_rows.append(('zero_click_rows', int((df['clicks'] == 0).sum())))
    if 'spent' in df.columns:
        summary_rows.append(('zero_spend_rows', int((df['spent'] == 0).sum())))

    summary_df = pd.DataFrame(summary_rows, columns=['metric', 'value'])

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    missing_df = missing.to_frame('missing_values') if not missing.empty else pd.DataFrame(columns=['missing_values'])

    dtype_breakdown = (
        df.dtypes.astype(str)
        .value_counts()
        .rename_axis('dtype')
        .reset_index(name='column_count')
    )

    return {
        'summary': summary_df,
        'missing': missing_df,
        'dtype_breakdown': dtype_breakdown
    }


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


def _coerce_schema(df: pd.DataFrame, parse_dates: Optional[List[str]] = None) -> pd.DataFrame:
    """Apply consistent dtype and datetime parsing rules after loading raw data."""
    df_coerced = df.copy()

    # Parse dates
    for col in (parse_dates or []):
        if col in df_coerced.columns:
            df_coerced[col] = pd.to_datetime(
                df_coerced[col],
                errors='coerce',
                dayfirst=True
            )

    # Ensure identifiers are treated as strings to avoid precision loss
    for col in IDENTIFIER_COLUMNS:
        if col in df_coerced.columns:
            df_coerced[col] = df_coerced[col].astype('Int64', errors='ignore') if df_coerced[col].dtype.kind in 'if' else df_coerced[col].astype(str)

    # Coerce numeric metrics
    for col in NUMERIC_COLUMNS:
        if col in df_coerced.columns:
            df_coerced[col] = pd.to_numeric(df_coerced[col], errors='coerce')

    return df_coerced


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

