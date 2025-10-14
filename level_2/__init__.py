import os
import json
import ast
import mysql.connector

#   Database Connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Developer123",   
    database="inato_data"
)
cursor = db_connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS application (
    id VARCHAR(100),
    therapeutic_area VARCHAR(255),
    created_at TIMESTAMP NULL,
    site_name VARCHAR(255),
    site_category VARCHAR(255)
);
""")

folder_path = "../processed"

for one_file in os.listdir(folder_path):
    if one_file.endswith(".json"):
        file_path = os.path.join(folder_path, one_file)
        print(file_path)

        with open(file_path, "r") as file:
            json_data = json.load(file)

        record_id = json_data.get("id")
        therapeutic_area = json_data.get("therapeutic_area")
        created_at = json_data.get("created_at")
        site_info = json_data.get("site")

        # Handle if 'site' is a string instead of dict
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
        """

        cursor.execute(insert_query, (record_id, therapeutic_area, created_at, site_name, site_category))

db_connection.commit()
cursor.close()
db_connection.close()

print("data inserted")
