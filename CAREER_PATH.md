# Data Analyst Career Path — How This Project Helps

This portfolio project is designed to showcase skills that hiring managers look for in **Data Analyst** roles. Below is how it maps to the career path and what you can say in interviews.

---

## What Data Analysts Do

- **Clean and transform data** from databases, CSVs, and APIs  
- **Write SQL** to answer business questions and build reports  
- **Analyse and visualise data** (Python/R, Excel, BI tools)  
- **Communicate insights** to stakeholders with clear recommendations  

---

## How This Project Demonstrates Each Skill

| Skill | Where in This Project |
|-------|------------------------|
| **SQL** | `sql_queries/`: basic queries, aggregations, JOINs, subqueries, window functions, business reports, RFM and cohort-style analytics |
| **Data cleaning** | `02_data_cleaning.py`: null checks, duplicates, types, outliers; `reports/data_quality_report.md` |
| **Exploratory analysis** | `03_exploratory_analysis.py` and notebook: revenue by month, top customers/products, correlations |
| **Visualisation** | `04_visualisations.py`: 10 charts (bar, line, pie, heatmap, box) saved to `reports/charts/` |
| **Statistics** | `05_statistical_analysis.py`: descriptive stats, normality, ANOVA, t-test, correlation |
| **Segmentation** | `06_customer_segmentation.py`: RFM + K-Means (Champions, Loyal, At Risk, Lost) |
| **Forecasting** | `07_sales_forecasting.py`: linear regression on monthly revenue, MAE/RMSE, Jan–Mar 2025 forecast |
| **Business sense** | `reports/summary_report.md` and notebook Section 9: recommendations and KPIs |
| **Testing** | `tests/`: database integrity, query correctness, analysis outputs |

---

## Typical Career Progression

1. **Junior Data Analyst** — Dashboards, ad-hoc SQL, cleaning and reporting (this project fits here).  
2. **Data Analyst** — Own domains (e.g. sales, marketing), A/B analysis, more advanced SQL and Python.  
3. **Senior Data Analyst** — Lead projects, define metrics, mentor juniors, work with engineering on pipelines.  
4. **Analytics Manager / BI Lead** — Prioritise work, stakeholder management, tooling and standards.  

*Some analysts later move into **Data Scientist** (more ML/modeling) or **Data Engineer** (pipelines, warehouses).*

---

## What to Say in Interviews

- **“Walk me through a project.”**  
  Use this repo: “I built an end-to-end analytics system for a simulated Nairobi e-commerce business: SQLite schema, seed data, SQL reports (revenue, churn, RFM), Python for cleaning, EDA, visualisations, segmentation with K-Means, and a simple sales forecast. I wrote tests and documented findings and recommendations.”  

- **“How do you ensure data quality?”**  
  Point to `02_data_cleaning.py` and `data_quality_report.md`: null checks, duplicates, outliers (IQR), type casting, and validation in tests.  

- **“How would you segment customers?”**  
  Describe RFM (Recency, Frequency, Monetary) and K-Means in `06_customer_segmentation.py`, and how you’d use segments (e.g. win-back for At Risk, rewards for Champions).  

---

## Next Steps to Grow

- Add a **BI dashboard** (e.g. Streamlit, Dash, or Power BI) on top of the same data.  
- Use **Git** properly: commit per task, clear messages, and a clean README (you already have one).  
- Practice **presenting** the project in 5 minutes (problem → data → methods → insights → recommendations).  
- Learn **version control** and **reproducible environments** (e.g. `requirements.txt`, virtualenv) — this project already uses them.  

---

*Author: Davis Kunyu Wamalwa | GitHub: daviesqunyu*
