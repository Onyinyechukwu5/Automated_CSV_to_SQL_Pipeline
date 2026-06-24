"""
scheduler.py — Weekly Auto-Run
Fires run_pipeline() every Monday at 08:00.
Keep this script running in the background (or use Windows Task Scheduler).
"""

import schedule
import time
import logging
from pipeline import run_pipeline

log = logging.getLogger(__name__)


def main():
    print("Scheduler started — pipeline will run every Monday at 08:00.")
    print("Press Ctrl+C to stop.\n")

    # ── Schedule: every Monday at 08:00 ──────────────
    schedule.every().monday.at("08:00").do(run_pipeline)

    # ── Uncomment the line below to test every minute ─
    # schedule.every(1).minutes.do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(30)  # check every 30 seconds


if __name__ == "__main__":
    main()
