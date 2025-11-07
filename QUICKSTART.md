# Quick Start Guide

## 🚀 Getting Started with Social Media Campaign Performance Tracker

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Add Your Data

1. Place your raw campaign data file in `data/raw/` directory
2. Supported formats: CSV (.csv) or Excel (.xlsx, .xls)
3. Rename it to `campaign_data.csv` or update the path in notebooks

### Step 3: Run Analysis Notebooks

Execute the notebooks in order:

1. **01_data_exploration.ipynb**
   - Explore your data structure
   - Understand data quality
   - Identify missing values

2. **02_data_cleaning.ipynb**
   - Clean the data
   - Calculate performance metrics (CTR, CPC, ROI, etc.)
   - Save cleaned data

3. **03_analysis.ipynb**
   - Perform campaign performance analysis
   - Identify top performers
   - Analyze by dimensions (campaign, age, device, region, etc.)

4. **04_visualizations.ipynb**
   - Create visualizations
   - Generate charts and graphs
   - Save figures to `outputs/figures/`

5. **05_dashboard_prep.ipynb**
   - Prepare data for dashboard
   - Export final dataset

### Step 4: Launch Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser automatically.

### Step 5: Explore Dashboard

The dashboard includes:
- **Overview**: Campaign KPIs and summary
- **Campaign Analysis**: Performance by dimensions
- **Performance Metrics**: Detailed metric analysis
- **Top Performers**: Best performing campaigns/ads
- **Recommendations**: Actionable insights

## 📊 Expected Data Columns

Your data should include columns such as:

### Required:
- Date/Time (for time series analysis)
- Impressions
- Clicks
- Spend/Cost

### Optional but Recommended:
- Reach
- Engagements
- Conversions
- Revenue
- Campaign name/ID
- Demographics (age, gender, device, region)

## 🛠️ Troubleshooting

### Data Not Loading
- Check file path in notebooks
- Verify file format (CSV or Excel)
- Check file encoding (try UTF-8)

### Missing Metrics
- Ensure required columns are present (impressions, clicks, spend)
- Check column names match expected formats
- Review data cleaning notebook output

### Dashboard Not Showing Data
- Run all notebooks in order
- Check that `data/processed/dashboard_data.csv` exists
- Verify data file paths in dashboard code

## 📝 Notes

- All processed data is saved in `data/processed/`
- Visualizations are saved in `outputs/figures/`
- You can customize the analysis in the `src/` modules

## 🔗 Resources

- [Pandas Documentation](https://pandas.pydata.org/)
- [Plotly Documentation](https://plotly.com/python/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

Happy Analyzing! 📈

