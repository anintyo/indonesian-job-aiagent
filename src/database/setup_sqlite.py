import json
import sqlite3
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from src.utils.salary_parser import parse_salary

JSONL_PATH = "data/raw/jobs.jsonl"
DB_PATH = "data/jobs.db"


def setup():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company_name TEXT,
            location TEXT,
            work_type TEXT,
            salary TEXT,
            salary_min INTEGER,
            salary_max INTEGER,
            job_description TEXT,
            scrape_timestamp TEXT
        )
    """)

    with open(JSONL_PATH, "r") as f:
        for line in f:
            job = json.loads(line)
            salary_min, salary_max = parse_salary(job.get("salary"))

            cursor.execute("""
                INSERT INTO jobs (
                    job_title, company_name, location, work_type,
                    salary, salary_min, salary_max,
                    job_description, scrape_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.get("job_title"),
                job.get("company_name"),
                job.get("location"),
                job.get("work_type"),
                job.get("salary"),
                salary_min,
                salary_max,
                job.get("job_description"),
                job.get("_scrape_timestamp"),
            ))

    conn.commit()
    conn.close()
    print(f"Done. Database saved to {DB_PATH}")


if __name__ == "__main__":
    setup()
