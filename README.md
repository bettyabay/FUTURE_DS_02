# Social Media Campaign Performance Tracker

📈 Analyze Facebook/Instagram ad campaign data to evaluate performance, engagement, CTR, and ROI. Develop dashboard storytelling skills using Python and Streamlit to present campaign optimization insights.

## 📁 Project Structure

```
FUTURE_DS_02/
│
├── data/
│   ├── raw/                    # Raw datasets (CSV/Excel files)
│   ├── processed/              # Cleaned and processed data
│   └── external/               # External reference data
│
├── notebooks/
│   ├── 01_data_exploration.ipynb      # Initial data exploration
│   ├── 02_data_cleaning.ipynb         # Data cleaning and preprocessing
│   ├── 03_analysis.ipynb              # Campaign performance analysis
│   ├── 04_visualizations.ipynb        # Create visualizations
│   └── 05_dashboard_prep.ipynb        # Prepare data for dashboard
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py      # Data cleaning and preprocessing functions
│   ├── analysis.py             # Analysis functions (CTR, ROI calculations)
│   ├── visualizations.py       # Visualization functions
│   └── utils.py                # Utility functions
│
├── dashboard/
│   ├── app.py                  # Main Streamlit dashboard application
│   ├── pages/                  # Multi-page dashboard pages (optional)
│   └── components/             # Reusable dashboard components
│
├── outputs/
│   ├── figures/                # Saved charts and visualizations
│   ├── reports/                # Generated reports (PDF/HTML)
│   └── exports/                # Exported data (CSV/Excel)
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # This file

```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Jupyter Notebook

```bash
python -m ipykernel install --user --name=social_media_analytics
```

### 3. Run Analysis

1. Start by exploring the data in `notebooks/01_data_exploration.ipynb`
2. Clean the data in `notebooks/02_data_cleaning.ipynb`
3. Perform analysis in `notebooks/03_analysis.ipynb`
4. Create visualizations in `notebooks/04_visualizations.ipynb`
5. Prepare dashboard data in `notebooks/05_dashboard_prep.ipynb`

### 4. Launch Dashboard

```bash
streamlit run dashboard/app.py
```

## 📊 Key Metrics to Analyze

- **Impressions**: Number of times ads were shown
- **Reach**: Unique number of people who saw ads
- **Clicks**: Number of clicks on ads
- **CTR (Click-Through Rate)**: (Clicks / Impressions) × 100
- **CPC (Cost Per Click)**: Total Spend / Clicks
- **CPM (Cost Per Mille)**: (Spend / Impressions) × 1000
- **Engagement Rate**: (Engagements / Impressions) × 100
- **ROI (Return on Investment)**: ((Revenue - Spend) / Spend) × 100
- **Conversion Rate**: (Conversions / Clicks) × 100

## 🎯 Deliverables

- [ ] Data exploration and cleaning notebook
- [ ] Performance analysis with key metrics
- [ ] Interactive visualizations
- [ ] Streamlit dashboard with:
  - Overview of campaign KPIs
  - Top-performing posts/ads
  - ROI summary
  - Interactive filters (by date, campaign, age, region, device, etc.)
  - Actionable recommendations
- [ ] Final report with insights and recommendations

## 🛠️ Tools Used

- **Python**: Data analysis and processing
- **Pandas**: Data manipulation
- **Matplotlib/Seaborn/Plotly**: Data visualization
- **Streamlit**: Interactive dashboard
- **Jupyter Notebooks**: Analysis and exploration

## 📝 Notes

- Place your raw data files in `data/raw/` directory
- Processed data will be saved in `data/processed/`
- All visualizations will be saved in `outputs/figures/`
- The dashboard can be customized in `dashboard/app.py`

## 🔗 Resources

- [Facebook Ads Performance Dataset - Kaggle](https://www.kaggle.com/datasets)
- [Social Media Ads - Kaggle](https://www.kaggle.com/datasets)
- [Marketing Campaign Data - Kaggle](https://www.kaggle.com/datasets)

---

**Task**: Social Media Campaign Performance Tracker  
**Skills**: Marketing Analytics, Campaign Optimization, Dashboard Storytelling  
**Tools**: Python, Jupyter Notebooks, Streamlit, Pandas, Plotly
