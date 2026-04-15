import argparse
import sqlite3
import requests
import gzip
import csv
import sys
import os
import glob

def main():
    parser = argparse.ArgumentParser(description="QC against Europe PMC and combine SQLite databases")
    parser.add_argument("--fetch_subset", type=str, choices=["true", "false", ""], nargs="?", const="true", default="false")
    args = parser.parse_args()

    is_subset = args.fetch_subset.lower() == "true"

    db_files = [f for f in glob.glob("*.sqlite") if f != "literature.sqlite" and not f.startswith("combined")]

    # Combine databases
    conn = sqlite3.connect("literature.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS literature (pmid INTEGER PRIMARY KEY, title TEXT, year INTEGER)")
    conn.commit()

    all_pmids = set()

    for db_file in db_files:
        print(f"Attaching and merging {db_file}...")
        cursor.execute(f"ATTACH DATABASE '{db_file}' AS chunk_db")
        cursor.execute("INSERT OR IGNORE INTO literature SELECT * FROM chunk_db.literature")
        conn.commit()

        # Get all PMIDs to check against PMC
        cursor.execute("SELECT pmid FROM chunk_db.literature")
        rows = cursor.fetchall()
        for row in rows:
            all_pmids.add(row[0])

        cursor.execute("DETACH DATABASE chunk_db")

    conn.commit()
    conn.close()

    print(f"Total PMIDs in final database: {len(all_pmids)}")

    # Download Europe PMC mapping
    pmc_url = "https://ftp.ebi.ac.uk/pub/databases/pmc/DOI/PMID_PMCID_DOI.csv.gz"
    pmc_filename = "PMID_PMCID_DOI.csv.gz"
    print("Downloading Europe PMC index...")

    if not os.path.exists(pmc_filename):
        response = requests.get(pmc_url, stream=True)
        response.raise_for_status()
        with open(pmc_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    print("Cross-referencing against Europe PMC index...")
    pmc_pmids = set()

    with gzip.open(pmc_filename, 'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pmid_str = row.get("PMID")
            if pmid_str:
                try:
                    pmid = int(pmid_str)
                    if is_subset:
                        if pmid in all_pmids:
                            pmc_pmids.add(pmid)
                    else:
                        pmc_pmids.add(pmid)
                except ValueError:
                    pass

    # Clean up PMC file
    os.remove(pmc_filename)

    intersection = all_pmids.intersection(pmc_pmids)
    missing = all_pmids - pmc_pmids

    with open("qc_report.txt", "w") as f:
        f.write(f"Total PMIDs downloaded from PubMed: {len(all_pmids)}\n")
        f.write(f"Total PMIDs found in Europe PMC index: {len(intersection)}\n")
        f.write(f"Match rate: {len(intersection)/len(all_pmids)*100 if all_pmids else 0:.2f}%\n")
        f.write(f"Missing from Europe PMC: {len(missing)}\n")

    print(f"QC Report generated. PMIDs from PubMed: {len(all_pmids)}, Found in PMC: {len(intersection)}.")

if __name__ == "__main__":
    main()
