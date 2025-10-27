import os
import json

BASE_DIR = os.path.dirname(os.getcwd())
INPUT_FOLDER = os.path.join(BASE_DIR, "applications")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "processed")
PROCESSED_LOG = os.path.join(BASE_DIR, "processed_files.log")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


if os.path.exists(PROCESSED_LOG):
    with open(PROCESSED_LOG, "r") as logfile:
        processed_files = set(logfile.read().splitlines())
else:
    processed_files = set()

new_files_processed = []

for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json") and filename not in processed_files:
        file_path = os.path.join(INPUT_FOLDER, filename)
        data = {}

        with open(file_path) as f:
            line = f.read().strip()
            parts = line.split("|")
            for part in parts:
                part = part.strip()
                if "=" in part:
                    key, value = part.split("=", 1)
                    data[key.strip()] = value.strip()

        output_path = os.path.join(OUTPUT_FOLDER, filename)
        with open(output_path, "w") as result:
            json.dump(data, result, indent=4)

        new_files_processed.append(filename)

if new_files_processed:
    with open(PROCESSED_LOG, "a") as f:
        for name in new_files_processed:
            f.write(name + "\n")

print("[Level 1] All new files converted to JSON")
print(BASE_DIR)