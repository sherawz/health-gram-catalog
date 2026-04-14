import sqlite3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Literature DB")
    parser.add_argument("--fetch_subset", action="store_true")
    parser.add_argument("--data_source", type=str, default="zenodo")
    args = parser.parse_args()

    conn = sqlite3.connect("literature.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS literature (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)")
    cursor.execute("INSERT INTO literature (title, year) VALUES ('Double Helix', 1953)")
    cursor.execute("INSERT INTO literature (title, year) VALUES ('mRNA Vaccines', 2020)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
