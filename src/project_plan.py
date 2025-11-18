"""
Project planning helpers that capture the analytics objectives, KPI definitions,
and workflow outline for the marketing analytics task.
"""

from typing import Dict, List


ANALYTICS_OBJECTIVES: List[str] = [
    "Quantify overall campaign efficiency through spend, reach, and conversion KPIs.",
    "Highlight the audience segments (age, gender, interest clusters) that deliver the strongest ROI proxies.",
    "Surface operational issues (data gaps, zero-impression ads, approval bottlenecks) early in the workflow.",
    "Create a reusable dataset that can power both notebook-based analysis and BI dashboards."
]


METRIC_DEFINITIONS: List[Dict[str, str]] = [
    {
        "name": "CTR",
        "formula": "clicks / impressions",
        "insight": "Creative resonance & traffic efficiency"
    },
    {
        "name": "CPC",
        "formula": "spent / clicks",
        "insight": "Cost paid for each engaged visitor"
    },
    {
        "name": "CPM",
        "formula": "spent / impressions * 1000",
        "insight": "Cost to reach one thousand people"
    },
    {
        "name": "CPA_Total",
        "formula": "spent / total_conversion",
        "insight": "Blended acquisition cost"
    },
    {
        "name": "CPA_Approved",
        "formula": "spent / approved_conversion",
        "insight": "Cost to acquire approved customers/leads"
    },
    {
        "name": "Approval_Rate",
        "formula": "approved_conversion / total_conversion",
        "insight": "Lead quality and downstream pipeline health"
    },
    {
        "name": "ROAS",
        "formula": "revenue (or approved conversions proxy) / spent",
        "insight": "Return for each dollar invested"
    }
]


WORKFLOW_STEPS: List[Dict[str, str]] = [
    {
        "step": "1. Explore & Profile",
        "focus": "Validate schema, missing data, zero/negative values, and overall volume.",
        "notebook": "01_data_exploration"
    },
    {
        "step": "2. Clean & Engineer Metrics",
        "focus": "Standardise dtypes, create KPI columns, and export curated datasets.",
        "notebook": "02_data_cleaning"
    },
    {
        "step": "3. Deep-Dive Analysis",
        "focus": "Slice KPIs by campaign dimension to extract insights.",
        "notebook": "03_analysis"
    },
    {
        "step": "4. Visualise & Storytell",
        "focus": "Build charts/notebooks/BI dashboards that highlight findings.",
        "notebook": "04_visualizations / 05_dashboard_prep"
    }
]


def get_project_plan() -> Dict[str, List]:
    """Return the consolidated analytics plan."""
    return {
        "objectives": ANALYTICS_OBJECTIVES,
        "metric_definitions": METRIC_DEFINITIONS,
        "workflow": WORKFLOW_STEPS
    }


def metrics_dataframe():
    """Convenience accessor for presenting KPI definitions inside notebooks."""
    import pandas as pd  # local import to avoid hard dependency when unused

    return pd.DataFrame(METRIC_DEFINITIONS)

