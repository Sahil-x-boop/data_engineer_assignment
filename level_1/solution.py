import os
import json
from datetime import datetime

input_folder = "../applications"
output_folder = "../processed"
log_file = "processed_log.json"

os.makedirs(output_folder, exist_ok=True)

# Load already processed files log
if os.path.exists(log_file):
    with open(log_file, "r") as logf:
        processed_log = json.load(logf)
else:
    processed_log = {}

for filename in os.listdir(input_folder):
    if not filename.endswith(".json"):
        continue

    input_path = os.path.join(input_folder, filename)
    modified_time = os.path.getmtime(input_path)

    # Only process if file is new or modified
    if filename in processed_log and processed_log[filename] == modified_time:
        continue

    data = {}
    with open(input_path, "r") as f:
        line = f.read().strip()
        parts = line.split("|")
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                data[key.strip()] = value.strip()

    output_path = os.path.join(output_folder, filename)
    with open(output_path, "w") as out:
        json.dump(data, out, indent=4)

    processed_log[filename] = modified_time
    print(f"Processed: {filename}")


with open(log_file, "w") as logf:
    json.dump(processed_log, logf, indent=4)

print(f"\n[{datetime.now()}] All new files converted to JSON")
