import sqlite3
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Combine SQLite DBs")
    parser.add_argument("--db_files", nargs='+', required=True, help="List of SQLite database files to combine")
    parser.add_argument("--output", type=str, default="combined_catalog.sqlite")
    args = parser.parse_args()

    conn_main = sqlite3.connect(args.output)
    cursor_main = conn_main.cursor()

    flat_files = []
    for f in args.db_files:
        flat_files.extend(f.split(' '))

    for db_file in flat_files:
        if not os.path.exists(db_file):
            print(f"Warning: {db_file} does not exist, skipping.")
            continue

        print(f"Attaching and migrating {db_file}...")
        db_name = os.path.splitext(os.path.basename(db_file))[0]
        cursor_main.execute(f"ATTACH DATABASE '{db_file}' AS {db_name}")

        # Get tables
        cursor_main.execute(f"SELECT name FROM {db_name}.sqlite_master WHERE type='table'")
        tables = cursor_main.fetchall()

        for table in tables:
            table_name = table[0]
            # Copy table schema by reading from original db, creating in main, and copying data
            cursor_main.execute(f"SELECT sql FROM {db_name}.sqlite_master WHERE type='table' AND name='{table_name}'")
            schema = cursor_main.fetchone()[0]
            cursor_main.execute(schema)
            cursor_main.execute(f"INSERT INTO {table_name} SELECT * FROM {db_name}.{table_name}")

        conn_main.commit()
        cursor_main.execute(f"DETACH DATABASE {db_name}")

    conn_main.close()
    print(f"Successfully created {args.output}")

if __name__ == "__main__":
    main()
