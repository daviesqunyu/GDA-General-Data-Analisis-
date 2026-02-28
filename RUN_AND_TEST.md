# How to Run and Test This Project

Run all commands from the **project root**: `nairobi-business-analytics/`

---

## 1. Setup (one time)

```powershell
cd nairobi-business-analytics
pip install -r requirements.txt
```

*(Optional but recommended: create a virtual environment first with `python -m venv venv` then `venv\Scripts\activate` on Windows.)*

---

## 2. Create the database and data

```powershell
python database/seed_data.py
```

**Expected output:** Messages like "Inserted 500 customers", "Inserted 50 products", etc., and a summary of row counts. The file `database/nairobi_business.db` is created.

---

## 3. Run the analysis scripts (in any order after step 2)

| Command | What it does |
|--------|----------------|
| `python python_analysis/01_data_loading.py` | Loads all 6 tables from DB, prints shape and sample |
| `python python_analysis/02_data_cleaning.py` | Data quality checks, writes `reports/data_quality_report.md` |
| `python python_analysis/03_exploratory_analysis.py` | EDA: revenue by month, top customers/products, correlations |
| `python python_analysis/04_visualisations.py` | Creates 10 charts in `reports/charts/` |
| `python python_analysis/05_statistical_analysis.py` | Descriptive stats, normality, ANOVA, t-test |
| `python python_analysis/06_customer_segmentation.py` | RFM + K-Means, saves segment charts |
| `python python_analysis/07_sales_forecasting.py` | Linear regression forecast, saves forecast chart |

**Example — run everything in sequence:**

```powershell
python python_analysis/01_data_loading.py
python python_analysis/02_data_cleaning.py
python python_analysis/03_exploratory_analysis.py
python python_analysis/04_visualisations.py
python python_analysis/05_statistical_analysis.py
python python_analysis/06_customer_segmentation.py
python python_analysis/07_sales_forecasting.py
```

---

## 4. Run the tests

**Option A — unittest (no extra install):**

```powershell
python -m unittest tests.test_database tests.test_queries tests.test_analysis -v
```

**Option B — pytest (after `pip install pytest`):**

```powershell
python -m pytest tests/ -v
```

**Expected:** All tests pass (e.g. “OK” or “passed”). Tests depend on the database existing and, for chart tests, on having run `04_visualisations.py` at least once.

---

## 5. Open the Jupyter notebook

```powershell
jupyter notebook notebooks/full_analysis_walkthrough.ipynb
```

Or from VS Code / Cursor: open `notebooks/full_analysis_walkthrough.ipynb` and run all cells. Ensure the kernel is using the same Python where you installed `requirements.txt`.

---

## Quick checklist

| Step | Command | Done? |
|------|---------|--------|
| 1 | `pip install -r requirements.txt` | |
| 2 | `python database/seed_data.py` | |
| 3 | Run any of the 7 scripts in `python_analysis/` | |
| 4 | `python -m unittest tests.test_database tests.test_queries tests.test_analysis -v` | |
| 5 | `jupyter notebook notebooks/full_analysis_walkthrough.ipynb` | |

---

## Troubleshooting

- **“Database not found”** → Run `python database/seed_data.py` first.
- **“No module named 'matplotlib'”** (or similar) → Run `pip install -r requirements.txt`.
- **Tests fail** → Ensure you’re in the project root and the database exists; for chart tests, run `python python_analysis/04_visualisations.py` once.
