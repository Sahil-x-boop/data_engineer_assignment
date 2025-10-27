import os
import json
import ast
from database_connection import get_connection

BASE_DIR = os.path.dirname(os.getcwd())
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")

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

inserted_count = 0

for filename in os.listdir(PROCESSED_FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(PROCESSED_FOLDER, filename)
        with open(file_path, "r") as file:
            json_data = json.load(file)

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

        # Check if record already exists
        cursor.execute("SELECT COUNT(*) FROM application WHERE id=%s", (record_id,))
        if cursor.fetchone()[0] > 0:
            continue

        insert_query = """
        INSERT INTO application (id, therapeutic_area, created_at, site_name, site_category)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (record_id, therapeutic_area, created_at, site_name, site_category))
        inserted_count += 1

db_connection.commit()
cursor.close()
db_connection.close()

print(f"[Level 2] {inserted_count} new records inserted successfully!")
