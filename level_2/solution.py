import os
import json
import ast
from database_connection import get_connection

processed_folder = "../processed"
log_file = "inserted_log.json"

# Load existing inserted files log
if os.path.exists(log_file):
    with open(log_file, "r") as logf:
        inserted_log = json.load(logf)
else:
    inserted_log = {}

db_connection = get_connection()
cursor = db_connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS application (
    id VARCHAR(100) PRIMARY KEY,
    therapeutic_area VARCHAR(255),
    created_at TIMESTAMP NULL,
    site_name VARCHAR(255),
    site_category VARCHAR(255)
);
""")

for filename in os.listdir(processed_folder):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(processed_folder, filename)
    modified_time = os.path.getmtime(file_path)

    # Skip if already inserted and unmodified
    if filename in inserted_log and inserted_log[filename] == modified_time:
        continue

    with open(file_path, "r") as f:
        json_data = json.load(f)

    record_id = json_data.get("id")
    therapeutic_area = json_data.get("therapeutic_area")
    created_at = json_data.get("created_at")
    site_info = json_data.get("site")

    if isinstance(site_info, str):
        try:
            site_info = ast.literal_eval(site_info)
        except Exception:
            site_info = {}

    if not isinstance(site_info, dict):
        site_info = {}

    site_name = site_info.get("site_name")
    site_category = site_info.get("site_category")

    insert_query = """
    INSERT INTO application (id, therapeutic_area, created_at, site_name, site_category)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        therapeutic_area = VALUES(therapeutic_area),
        created_at = VALUES(created_at),
        site_name = VALUES(site_name),
        site_category = VALUES(site_category);
    """

    cursor.execute(insert_query, (record_id, therapeutic_area, created_at, site_name, site_category))
    inserted_log[filename] = modified_time
    print(f"Inserted/Updated: {filename}")

db_connection.commit()
cursor.close()
db_connection.close()

# Save log
with open(log_file, "w") as logf:
    json.dump(inserted_log, logf, indent=4)

print("All new data inserted successfully!")
