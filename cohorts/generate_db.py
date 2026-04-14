import sqlite3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Cohorts DB")
    parser.add_argument("--fetch_subset", action="store_true")
    parser.add_argument("--data_source", type=str, default="zenodo")
    args = parser.parse_args()

    conn = sqlite3.connect("cohorts.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cohorts (id INTEGER PRIMARY KEY, cohort_name TEXT, size INTEGER)")
    cursor.execute("INSERT INTO cohorts (cohort_name, size) VALUES ('PGP', 10000)")
    cursor.execute("INSERT INTO cohorts (cohort_name, size) VALUES ('UK Biobank', 500000)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
