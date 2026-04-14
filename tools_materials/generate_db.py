import sqlite3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Tools/Materials DB")
    parser.add_argument("--fetch_subset", action="store_true")
    parser.add_argument("--data_source", type=str, default="zenodo")
    args = parser.parse_args()

    conn = sqlite3.connect("tools_materials.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tools_materials (id INTEGER PRIMARY KEY, item_name TEXT, category TEXT)")
    cursor.execute("INSERT INTO tools_materials (item_name, category) VALUES ('CRISPR Cas9 Kit', 'Material')")
    cursor.execute("INSERT INTO tools_materials (item_name, category) VALUES ('Sequencer', 'Tool')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
