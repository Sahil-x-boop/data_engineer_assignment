# Data Engineer Take-Home Assignment

## Automated ETL + Analytics Pipeline (Python + MySQL + Cron)

This project implements a 3-level data pipeline that automatically:
1. Converts raw application files into structured JSONs  
2. Inserts new data into a MySQL database  
3. Runs analytical SQL queries  
4. Repeats automatically every 3 hours using a Linux cron job  

It simulates a real-world data ingestion and analytics pipeline, similar to those used in production-grade data engineering systems.

---

## Project Overview

| Level | Component | Description |
|--------|------------|-------------|
| Level 1 | `process_raw.py` | Converts raw pipe-separated data into JSON files |
| Level 2 | `insert_db.py` | Inserts processed data into MySQL database |
| Level 3 | `queries.sql` + `scheduler.py` | Runs analytics queries and automates the entire ETL process |
| Automation | Cron job | Schedules the pipeline to run every 3 hours automatically |

---

## Folder Structure
```
data_engineer_assignment/
│
├── applications/                # raw incoming .json-like files
├── processed/                   # structured JSONs (output of Level 1)
│
├── level_1/
│   └── process_raw.py
│
├── level_2/
│   ├── insert_db.py
│   └── database_connection.py
│
├── level_3/
│   ├── queries.sql
│   └── scheduler.py
│
├── processed_files.log          # tracks which files have been processed
├── level_3/pipeline.log         # logs all cron/scheduler activity
└── README.md
```

---

## Level 1 — Data Conversion (`process_raw.py`)

### Purpose
This script reads raw application files from `applications/`, where each file contains a single line formatted as:
```
id=123|therapeutic_area=Oncology|created_at=2023-02-14 09:00:00|site={"site_name":"Apollo","site_category":"Academic"}
```

The script:
- Parses each key=value pair  
- Converts it into a structured JSON object  
- Saves it in `/processed/`  
- Records the processed filename in `processed_files.log` to avoid duplicate processing  

### Run Manually
```bash
python3 level_1/process_raw.py
```

### Example Output
```
[Level 1] All new files converted to JSON
```

---

## Level 2 — Database Insertion (`insert_db.py`)

### Purpose
This script inserts the processed JSON files into a MySQL database called `inato_data`.

### Steps Performed
1. Connects to MySQL using credentials stored in `database_connection.py`
2. Creates a table named `application` if it doesn't already exist
3. Reads each JSON file in the `processed/` directory
4. Inserts only new records based on unique `id` values

### Run Manually
```bash
python3 level_2/insert_db.py
```

### Example Output
```
[Level 2] 5 new records inserted successfully!
```

### Database Table Structure

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(100) | Unique identifier |
| therapeutic_area | VARCHAR(255) | Trial type (e.g., Oncology) |
| created_at | TIMESTAMP | Record creation time |
| site_name | VARCHAR(255) | Name of the site |
| site_category | VARCHAR(255) | Site category (e.g., Academic) |

---

## Level 3 — SQL Analysis (`queries.sql`)

### Purpose
This file contains analytical SQL queries that extract insights from the `application` table.

### Query 1 — Oncology Ratio
Finds the ratio of oncology trials to total trials for each academic site.
```sql
SELECT 
    site_name,     
    SUM(therapeutic_area = 'Oncology') / COUNT(*) AS oncology_rate 
FROM application 
WHERE site_category = 'Academic' 
GROUP BY site_name;
```

### Query 2 — Active Sites Within 14 Days
Finds sites with at least 10 applications submitted within 14 days of their first submission.
```sql
WITH first_app AS (
    SELECT site_name, MIN(created_at) AS first_date
    FROM application
    GROUP BY site_name
)
SELECT a.site_name
FROM application a
JOIN first_app f
  ON a.site_name = f.site_name
WHERE a.created_at <= DATE_ADD(f.first_date, INTERVAL 14 DAY)
GROUP BY a.site_name
HAVING COUNT(*) >= 10;
```

---

## Level 3 — Scheduler (`scheduler.py`)

### Purpose
Automates the entire ETL process by:
1. Running Level 1 (data conversion)
2. Running Level 2 (database insertion)
3. Executing the SQL queries in `queries.sql`
4. Logging all activity into `pipeline.log`

### Run Manually
```bash
python3 level_3/scheduler.py
```

### Example Output
```
[2025-10-24 18:46:32.450257] All new files converted to JSON
All new data inserted successfully!
[2025-10-24 18:46:32.841066] Running query.sql...
[2025-10-24 18:46:32.846725] Pipeline completed successfully!
```

---

## Automation Using Cron Job

### Purpose
To automate the pipeline to run every 3 hours.

### Steps to Set Up

1. Open the crontab:
```bash
crontab -e
```

2. Add the following line:
```bash
0 */3 * * * /home/developer/.pyenv/shims/python3 /home/developer/Workspace_Projects/data_engineer_assignment/level_3/scheduler.py >> /home/developer/Workspace_Projects/data_engineer_assignment/level_3/pipeline.log 2>&1
```

3. Save and exit.

This means:
- The pipeline runs every 3 hours
- Logs are stored in `pipeline.log`

To verify the cron job is active:
```bash
crontab -l
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Access denied for user 'developer'@'localhost' | Incorrect MySQL username/password | Update credentials in `database_connection.py` |
| ModuleNotFoundError | Missing dependencies | Install using `pip install mysql-connector-python` |
| No JSON files created | `applications/` folder empty | Add raw input files before running Level 1 |
| Data not updating | Duplicate file entries | Clear or check `processed_files.log` |

---

## Complete Pipeline Flow

1. Raw data → `applications/`
2. Level 1 converts raw data → `processed/` (JSON format)
3. Level 2 reads JSON → inserts into `inato_data.application` table
4. Level 3 runs SQL analytics → saves outputs/logs
5. Cron job executes the pipeline automatically every 3 hours

---

## Dependencies

- Python 3.10+
- MySQL Server
- Required Python modules:
```bash
pip install mysql-connector-python
```

---

## Run the Whole Pipeline Manually (Without Cron)
```bash
python3 level_3/scheduler.py
```

---

## Logs

- `processed_files.log` → Tracks which files were already processed
- `level_3/pipeline.log` → Stores all run-time logs of ETL + queries