# Automated CSV to SQL Weekly Pipeline

An automated data engineering pipeline that ingests CSV files from a local folder, cleans and transforms the data, and loads it into a PostgreSQL database — running hands-free every Monday at 08:00.

Built with Python and Jupyter Notebook on Windows 11.

## Project Overview

This pipeline was built as a portfolio project to demonstrate core data engineering skills: ingestion, transformation, deduplication, loading, scheduling, and logging — all without manual intervention.

The pipeline processes 11 CSV datasets covering business domains including sales, HR, inventory, finance, and operations.

## Datasets

| File | Description |
|------|-------------|
| `customer_orders.csv` | Customer purchase records |
| `employees.csv` | Employee master data |
| `inventory.csv` | Stock and product inventory |
| `payroll.csv` | Employee payroll records |
| `product_returns.csv` | Returned product transactions |
| `project_tasks.csv` | Internal project task tracking |
| `sales_q1.csv` | Q1 sales transactions |
| `store_branches.csv` | Store branch information |
| `supplier_invoices.csv` | Supplier billing records |
| `training_records.csv` | Staff training history |
| `website_traffic.csv` | Web analytics data |

## Project Structure

```
C:\Automated pipeline\
├── Raw data\                        ← Drop CSV files here
├── CSV_to_SQL_Weekly_Pipeline.ipynb ← Main notebook (run this)
├── pipeline.log                     ← Audit log (auto-created)
└── processed_files.txt              ← Deduplication tracker (auto-created)
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| Jupyter Notebook | Development environment |
| pandas | CSV ingestion and transformation |
| SQLAlchemy | Database connection layer |
| psycopg2 | PostgreSQL driver |
| PostgreSQL | Target database (`Pipeline_DB`) |
| schedule | Weekly automation |
| logging | Audit trail |
| Windows 11 | Operating system |

---

## How It Works

```
Raw data\ folder
      │
      ▼
  Scan for CSVs
      │
      ▼
  Skip already-loaded files  ──► processed_files.txt
      │
      ▼
  Transform
  ├── Standardise column names (lowercase + underscores)
  ├── Drop duplicate rows
  ├── Drop empty rows
  ├── Fill nulls (strings → "", numbers → 0)
  ├── Parse date columns (DD-MM-YYYY)
  └── Add loaded_at audit timestamp
      │
      ▼
  Load to PostgreSQL (Pipeline_DB)
      │
      ▼
  Log result to pipeline.log
```

Each CSV file is loaded into its own table, named after the file (e.g. `customer_orders.csv` → table `customer_orders`).

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- PostgreSQL installed and running locally

### 1. Install dependencies
```bash
pip install pandas sqlalchemy psycopg2-binary schedule
```

### 2. Create the database
Open **SQL Shell (psql)**, press Enter through the prompts to connect, then run:
```sql
CREATE DATABASE "Pipeline_DB";
```

### 3. Configure credentials
In **Cell 2** of the notebook, fill in your PostgreSQL details:
```python
PG_USER     = "your_username"
PG_PASSWORD = "your_password"
PG_HOST     = "localhost"
PG_PORT     = "5432"
PG_DB       = "Pipeline_DB"
```
### 4. Run the notebook
Open `CSV_to_SQL_Weekly_Pipeline.ipynb` and run cells top to bottom:

| Cell | What it does |
|------|-------------|
| Cell 1 | Sets working directory — run first every session |
| Cell 2 | Imports, config, logging setup |
| Cell 3 | Deduplication helper functions |
| Cell 4 | Transform function |
| Cell 5 | Runs the pipeline immediately |
| Cell 6 | Starts the weekly scheduler (Monday 08:00) |
| Cell 7 | Preview loaded tables (optional) |

---

## Sample Log Output

```
2026-06-24 23:11:34  [INFO]  Pipeline started
2026-06-24 23:11:34  [INFO]  Reading  →  customer_orders.csv
2026-06-24 23:11:34  [INFO]    Shape before transform: (12, 8)
2026-06-24 23:11:34  [INFO]    Duplicates removed: 2
2026-06-24 23:11:34  [INFO]    Shape after  transform: (10, 9)
2026-06-24 23:11:34  [INFO]  LOADED  customer_orders.csv  →  table 'customer_orders'  (10 rows)
2026-06-24 23:11:35  [INFO]  Pipeline finished — 11 loaded, 0 skipped.
```

---

## Key Features

- **Deduplication** — files already loaded are tracked and never inserted twice
- **Audit trail** — every run, row count, and error is written to `pipeline.log`
- **Automatic scheduling** — runs every Monday at 08:00 via the `schedule` library
- **Fault tolerance** — bad files are caught with `try/except` and logged without stopping the pipeline
- **Multi-table loading** — each CSV lands in its own PostgreSQL table automatically

---

## Future Improvements

Email alerts after each run using smtplib
Cloud storage integration (AWS S3 or Azure Blob)
Data quality checks before loading
Streamlit dashboard to visualise loaded data
Migration to Apache Airflow for production scheduling

## Author
Onyinye Chukwu
Built as a Data Engineering learning project.
