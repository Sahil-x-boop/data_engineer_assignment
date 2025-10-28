import subprocess
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.getcwd())
LEVEL1 = os.path.join(BASE_DIR, "level_1", "process_raw.py")
LEVEL2 = os.path.join(BASE_DIR, "level_2", "insert_into_database.py")
QUERY_SQL = os.path.join(BASE_DIR, "level_3", "queries.sql")
LOG_FILE = os.path.join(BASE_DIR, "level_3", "pipeline.log")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        log(result.stdout)
    except subprocess.CalledProcessError as e:
        log(f"ERROR: {e.stderr}")

log("Starting automated pipeline...")


subprocess.run(["python3", LEVEL1])
log("All new files converted to JSON")

subprocess.run(["python3", LEVEL2])
log("All new data inserted successfully!")

# Run SQL queries using .my.cnf credentials
try:
    subprocess.run(["mysql", "inato_data", "-e", f"source {QUERY_SQL}"], check=True)
    log("Query.sql executed successfully")
except subprocess.CalledProcessError as e:
    log(f"SQL ERROR: {e}")

log("Pipeline completed successfully!\n")
