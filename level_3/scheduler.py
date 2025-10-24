import subprocess
from datetime import datetime

print(f"\n[{datetime.now()}] Starting automated pipeline...")

subprocess.run(["python3", "/home/developer/Workspace_Projects/data_engineer_assignment/level_1/solution.py"])

subprocess.run(["python3", "/home/developer/Workspace_Projects/data_engineer_assignment/level_2/solution.py"])

print(f"[{datetime.now()}] Running query.sql...")
subprocess.run([
    "mysql",
    "-u", "root",
    "-pHarman@123",
    "inato_data",
    "-e", "source /home/developer/Workspace_Projects/data_engineer_assignment/level_3/queries.sql"
])

print(f"[{datetime.now()}] Pipeline completed successfully!\n")