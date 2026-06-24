"""
setup_task_scheduler.py
Registers a Windows Task Scheduler job to run scheduler.py every Monday at 08:00.
Run this ONCE as Administrator.
"""

import subprocess
import sys
from pathlib import Path

TASK_NAME   = "CSV_Pipeline_Weekly"
SCRIPT_PATH = r"C:\Automated pipeline\scheduler.py"
PYTHON_EXE  = sys.executable  # uses whichever Python is currently active


def register_task():
    # Build the schtasks command
    cmd = [
        "schtasks", "/Create", "/F",
        "/TN", TASK_NAME,
        "/TR", f'"{PYTHON_EXE}" "{SCRIPT_PATH}"',
        "/SC", "WEEKLY",
        "/D",  "MON",
        "/ST", "08:00",
    ]

    print(f"Registering task: {TASK_NAME}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅  Task registered successfully.")
        print("    It will fire every Monday at 08:00.")
        print(f"    Manage it in: Task Scheduler → {TASK_NAME}")
    else:
        print("❌  Failed to register task.")
        print(result.stderr)
        print("\nTip: run this script as Administrator.")


if __name__ == "__main__":
    register_task()
