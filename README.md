# Nairobi Business Intelligence & Sales Analytics System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.1-orange.svg)](https://pandas.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

## Project Overview

The **Nairobi Business Intelligence & Sales Analytics System** is a full end-to-end data analytics project simulating a real Kenyan e-commerce/retail business operating in Nairobi. It demonstrates production-quality data engineering, SQL reporting, Python data analysis, statistical inference, and business intelligence workflows.

This project is designed as a portfolio piece for Data Analyst roles. It showcases the complete data lifecycle: database design, ETL, exploratory data analysis (EDA), statistical analysis, customer segmentation (RFM + K-Means), sales forecasting, and actionable business recommendations—all using realistic Kenyan business context (Nairobi neighbourhoods, M-Pesa payments, KSh currency).

## Skills Demonstrated

- **SQL**: Schema design, aggregations, JOINs, subqueries, window functions, business KPI reports, cohort analysis, RFM segmentation
- **Python**: pandas, numpy, sqlite3, data loading and transformation
- **Data Cleaning**: Null handling, duplicate detection, outlier treatment (IQR), type casting
- **Exploratory Data Analysis (EDA)**: Distributions, correlations, descriptive statistics
- **Data Visualisation**: matplotlib, seaborn, plotly — bar, line, pie, heatmap, box plots, scatter
- **Statistical Analysis**: Descriptive stats, Shapiro-Wilk normality, ANOVA, t-tests, Pearson correlation
- **Machine Learning**: K-Means clustering (customer segmentation), Linear Regression (sales forecasting)
- **Business Intelligence**: KPIs, revenue reports, churn analysis, payment and delivery performance
- **Testing**: unittest/pytest for database integrity, query correctness, and analysis functions
- **Documentation**: README, inline comments, Jupyter narrative, data quality reports

## Tech Stack

| Component | Technology |
|-----------|------------|
| Database | SQLite 3 |
| Language | Python 3.9+ |
| Data Manipulation | pandas, numpy |
| Visualisation | matplotlib, seaborn, plotly |
| Statistics | scipy, scikit-learn |
| Notebook | Jupyter |
| Testing | pytest |

## Database Schema

The system uses **6 tables**:

| Table | Description |
|-------|-------------|
| **customers** | Customer demographics, location (Nairobi neighbourhoods), type (Individual/SME/Corporate), registration date, active status |
| **products** | Product name, category, unit/cost price, stock, supplier |
| **orders** | Order date, delivery date, status, payment method, delivery zone, total amount, discount |
| **order_items** | Line items: product, quantity, unit price, subtotal per order |
| **payments** | Payment method, amount, date, transaction reference (e.g. M-Pesa code), status |
| **customer_support** | Ticket type, status, satisfaction score (1–5) |

Relationships: `orders` → `customers`; `order_items` → `orders`, `products`; `payments` → `orders`; `customer_support` → `customers`.

## Project Structure

```
nairobi-business-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── database/
│   ├── schema.sql
│   ├── seed_data.py
│   └── nairobi_business.db
├── sql_queries/
│   ├── 01_basic_queries.sql
│   ├── 02_aggregations.sql
│   ├── 03_joins.sql
│   ├── 04_subqueries.sql
│   ├── 05_window_functions.sql
│   ├── 06_business_reports.sql
│   └── 07_advanced_analytics.sql
├── python_analysis/
│   ├── 01_data_loading.py
│   ├── 02_data_cleaning.py
│   ├── 03_exploratory_analysis.py
│   ├── 04_visualisations.py
│   ├── 05_statistical_analysis.py
│   ├── 06_customer_segmentation.py
│   └── 07_sales_forecasting.py
├── notebooks/
│   └── full_analysis_walkthrough.ipynb
├── reports/
│   ├── summary_report.md
│   └── charts/
└── tests/
    ├── test_database.py
    ├── test_queries.py
    └── test_analysis.py
```

## How to Run and Test

**→ Full step-by-step guide: [RUN_AND_TEST.md](RUN_AND_TEST.md)**

Quick version:

1. **Clone and enter the project**
   ```bash
   git clone <your-repo-url> nairobi-business-analytics
   cd nairobi-business-analytics
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the database and seed data**
   ```bash
   python database/seed_data.py
   ```

5. **Run analysis scripts (optional)**
   ```bash
   python python_analysis/01_data_loading.py
   python python_analysis/02_data_cleaning.py
   python python_analysis/03_exploratory_analysis.py
   python python_analysis/04_visualisations.py
   python python_analysis/05_statistical_analysis.py
   python python_analysis/06_customer_segmentation.py
   python python_analysis/07_sales_forecasting.py
   ```

6. **Open the full analysis notebook**
   ```bash
   jupyter notebook notebooks/full_analysis_walkthrough.ipynb
   ```

7. **Run tests**
   ```bash
   python -m pytest tests/ -v
   ```

## Key Findings (from sample analysis)

- **Revenue seasonality**: Higher sales in Q4 (Nov–Dec) due to festive season; lower in Jan–Feb.
- **M-Pesa dominance**: Majority of transactions use M-Pesa, aligning with Kenyan payment behaviour.
- **Location concentration**: Westlands, CBD, and Karen contribute the most customers and revenue.
- **Customer segments**: RFM + K-Means identify Champions (high value, recent), Loyal, At Risk, and Lost segments for targeted campaigns.
- **Forecasting**: Linear trend from 2024 monthly revenue supports basic Jan–Mar 2025 revenue projections.
- **Support impact**: Resolution time and satisfaction scores vary by issue type; delivery and payment issues need priority.

## Charts Preview

Key visualisations (saved in `reports/charts/`):

- **monthly_revenue_bar.png** — Monthly revenue (Jan–Dec 2024)
- **revenue_trend_line.png** — Revenue trend with trend line
- **category_pie.png** — Revenue by product category
- **rfm_segments_scatter.png** — Customer segments (RFM + K-Means)
- **sales_forecast_chart.png** — Actual vs predicted vs forecast

## SQL Skills Covered

| File | Concepts |
|------|----------|
| 01_basic_queries.sql | SELECT, WHERE, ORDER BY, LIMIT |
| 02_aggregations.sql | GROUP BY, HAVING, COUNT, SUM, AVG, MIN, MAX |
| 03_joins.sql | INNER JOIN, LEFT JOIN, multi-table JOINs |
| 04_subqueries.sql | Subqueries, nested queries, EXISTS |
| 05_window_functions.sql | ROW_NUMBER, RANK, LAG, LEAD, running totals |
| 06_business_reports.sql | KPIs, revenue, CLV, churn, delivery performance |
| 07_advanced_analytics.sql | RFM, cohort analysis, basket analysis |

## Data Analyst Career Path

See **[CAREER_PATH.md](CAREER_PATH.md)** for how this project maps to Data Analyst skills, typical career progression (Junior → Senior → Analytics Manager), and what to say in interviews.

## Author

**Davis Kunyu Wamalwa**  
BSc Computer Science | CUEA 2025  
GitHub: [daviesqunyu](https://github.com/daviesqunyu)  
Email: daviskunyu@gmail.com
