"""
Utility functions for the project
"""

import pandas as pd
from typing import List, Optional


def display_data_info(df: pd.DataFrame):
    """
    Display comprehensive information about the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to analyze
    """
    print("=" * 50)
    print("DATASET INFORMATION")
    print("=" * 50)
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn Names:")
    for col in df.columns:
        print(f"  - {col}")
    
    print(f"\nData Types:")
    print(df.dtypes)
    
    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values!")
    
    print(f"\nFirst few rows:")
    print(df.head())
    
    print(f"\nSummary Statistics:")
    print(df.describe())


def format_currency(value: float, currency: str = "USD") -> str:
    """
    Format a number as currency
    
    Parameters:
    -----------
    value : float
        Value to format
    currency : str
        Currency symbol (default: "USD")
    
    Returns:
    --------
    str
        Formatted currency string
    """
    if currency == "USD":
        return f"${value:,.2f}"
    else:
        return f"{currency} {value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a number as percentage
    
    Parameters:
    -----------
    value : float
        Value to format
    decimals : int
        Number of decimal places (default: 2)
    
    Returns:
    --------
    str
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"

