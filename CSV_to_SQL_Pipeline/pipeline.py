"""
pipeline.py — CSV to SQL Ingestion & Loading
Scans the raw data folder, transforms each CSV, and loads it into the database.
"""
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

# ── Paths (edit here if your folders differ) ──────────────
RAW_DATA_PATH   = r"C:\Automated pipeline\Raw data"
LOG_FILE        = r"C:\Automated pipeline\pipeline.log"
PROCESSED_LOG   = r"C:\Automated pipeline\processed_files.txt"

# ── PostgreSQL connection — fill in your credentials ──────
PG_USER     = "Postgres"
PG_PASSWORD = "Postgres"
PG_HOST     = "localhost"       # or your server IP / RDS endpoint
PG_PORT     = "5432"
PG_DB       = "Pipeline_DB"

DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

print("✅  Config loaded.")
print(f"   Raw data  : {RAW_DATA_PATH}")
print(f"   Database  : {DB_URL}")
print(f"   Log file  : {LOG_FILE}")

# ──────────────────────────────────────────────
# HELPER — track already-processed files
# ──────────────────────────────────────────────

def load_processed_files() -> set:
    """Return filenames already loaded into the database."""
    if not os.path.exists(PROCESSED_LOG):
        return set()
    with open(PROCESSED_LOG, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def mark_file_processed(filename: str):
    """Append a filename to the processed-files tracker."""
    with open(PROCESSED_LOG, "a", encoding="utf-8") as f:
        f.write(filename + "\n")


print("✅  Helper functions defined.")



# ──────────────────────────────────────────────
# TRANSFORM
# ──────────────────────────────────────────────
def transform(df: pd.DataFrame, filename: str = "") -> pd.DataFrame:
    """Clean and standardise a raw DataFrame."""

    # 1. Standardise column names → lowercase with underscores
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(r"[^\w]+", "_", regex=True)
                  .str.strip("_")
    )

    # 2. Drop fully duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    log.info(f"  [{filename}] Duplicates removed: {before - len(df)}")

    # 3. Drop rows that are entirely empty
    df = df.dropna(how="all")

    # 4. Fill nulls: strings → empty string, numbers → 0
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("").str.strip()
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(0)

    # 5. Auto-detect and convert date columns
    date_keywords = ("date", "time", "dt", "created", "updated")
    for col in df.columns:
        if any(kw in col for kw in date_keywords):
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            except Exception:
                pass

    # 6. Audit column
    df["loaded_at"] = datetime.now().isoformat(timespec="seconds")

    return df


print("✅  Transform function defined.")


# ──────────────────────────────────────────────
# MAIN PIPELINE
# ──────────────────────────────────────────────
def run_pipeline():
    log.info("=" * 55)
    log.info("Pipeline started")

    raw_dir = Path(RAW_DATA_PATH)
    if not raw_dir.exists():
        log.error(f"Raw data folder not found: {raw_dir}")
        return

    csv_files = list(raw_dir.glob("*.csv"))
    if not csv_files:
        log.info("No CSV files found in raw data folder. Nothing to do.")
        return

    processed = load_processed_files()
    engine = create_engine(DB_URL)

    loaded_count = 0
    skipped_count = 0

    for csv_path in csv_files:
        filename = csv_path.name

        if filename in processed:
            log.info(f"SKIP  {filename}  (already loaded)")
            skipped_count += 1
            continue

        try:
            log.info(f"Reading  →  {filename}")
            df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip")
            log.info(f"  Shape before transform: {df.shape}")

            df = transform(df)
            log.info(f"  Shape after  transform: {df.shape}")

            # Derive table name from file stem for multi-file pipelines
            table = csv_path.stem.lower().replace(" ", "_")

            df.to_sql(table, engine, if_exists="append", index=False)
            mark_file_processed(filename)

            log.info(f"LOADED  {filename}  →  table '{table}'  ({len(df)} rows)")
            loaded_count += 1

        except Exception as e:
            log.error(f"FAILED  {filename}  —  {e}")

    log.info(
        f"Pipeline finished — {loaded_count} file(s) loaded, "
        f"{skipped_count} skipped."
    )
    log.info("=" * 55)


if __name__ == "__main__":
    run_pipeline()
