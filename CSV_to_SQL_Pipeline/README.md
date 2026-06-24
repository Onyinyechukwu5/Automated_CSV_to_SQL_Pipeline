# CSV → SQL Weekly Pipeline

A lightweight data engineering pipeline that automatically ingests CSV files from a local folder, cleans and transforms the data, and loads it into a SQL database — every Monday at 08:00, hands-free.

---

## Project Structure

```
C:\Automated pipeline\
├── Raw data\          ← Drop CSVs here
├── pipeline.py        ← Ingestion, transform & load logic
├── scheduler.py       ← Runs pipeline on a weekly schedule
├── setup_task_scheduler.py  ← One-time Windows Task Scheduler registration
├── pipeline.db        ← SQLite database (auto-created on first run)
├── pipeline.log       ← Audit log
└── processed_files.txt ← Deduplication tracker
```

---

## Setup

### 1. Install dependencies
```bash
pip install pandas sqlalchemy schedule psycopg2-binary
```

### 2. Configure paths
Open `pipeline.py` and confirm these match your environment:
```python
RAW_DATA_PATH = r"C:\Automated pipeline\Raw data"
LOG_FILE      = r"C:\Automated pipeline\pipeline.log"
DB_URL        = r"sqlite:///C:\Automated pipeline\pipeline.db"
```

To use **PostgreSQL** instead of SQLite, replace `DB_URL` with:
```python
DB_URL = "postgresql://username:password@localhost:5432/your_db"
```

### 3. Run manually (first test)
```bash
cd "C:\Automated pipeline"
python pipeline.py
```

### 4. Start the weekly scheduler
```bash
python scheduler.py
```
Keep this terminal open, or register it as a Windows Task (see below).

### 5. Register as a Windows Task (optional but recommended)
Run **as Administrator**:
```bash
python setup_task_scheduler.py
```
This registers the pipeline to run automatically every Monday at 08:00 — no terminal needed.

---

## How It Works

| Step | What happens |
|------|-------------|
| **Scan** | Finds all `.csv` files in `Raw data\` |
| **Deduplicate** | Skips files already loaded (tracked in `processed_files.txt`) |
| **Transform** | Cleans column names, drops dupes, fills nulls, fixes dates |
| **Load** | Inserts rows into SQLite/PostgreSQL via SQLAlchemy |
| **Log** | Records every run, file, row count, and error in `pipeline.log` |

---

## Testing

1. Drop a CSV into `Raw data\`
2. Run `python pipeline.py`
3. Open the database and confirm rows landed
4. Drop the **same** CSV again → confirm it is **not** loaded twice
5. Check `pipeline.log` for the full audit trail

### Quick scheduler test
In `scheduler.py`, swap the weekly schedule for a 1-minute one:
```python
# schedule.every().monday.at("08:00").do(run_pipeline)
schedule.every(1).minutes.do(run_pipeline)
```
Confirm it fires, then switch back.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| `pandas` | Read & transform CSV files |
| `sqlalchemy` | Connect to and write to SQL database |
| `sqlite3` | Default embedded database |
| `schedule` | Weekly automation |
| `logging` | Audit trail |
| `schtasks` | Windows Task Scheduler integration |

---

## Extending the Pipeline

- **Email alerts** — use `smtplib` to send a summary email after each run
- **Cloud upload** — push the DB or processed CSVs to AWS S3 with `boto3`
- **Dashboard** — visualise the loaded data with Streamlit
- **PostgreSQL** — swap the `DB_URL` for a production-grade database
