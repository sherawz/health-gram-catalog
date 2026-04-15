import argparse
import requests
import hashlib
import sqlite3
import gzip
from lxml import etree
import sys
import os

def verify_md5(filepath, expected_md5):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest() == expected_md5

def main():
    parser = argparse.ArgumentParser(description="Process a single PubMed chunk")
    parser.add_argument("--url", required=True)
    parser.add_argument("--md5", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--fetch_subset", type=str, choices=["true", "false", ""], nargs="?", const="true", default="false")
    args = parser.parse_args()

    is_subset = args.fetch_subset.lower() == "true"

    print(f"Downloading {args.filename}...")
    response = requests.get(args.url, stream=True)
    response.raise_for_status()

    with open(args.filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Verifying MD5 for {args.filename}...")
    if not verify_md5(args.filename, args.md5):
        print(f"MD5 mismatch for {args.filename}!")
        sys.exit(1)

    db_filename = f"{args.filename}.sqlite"
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS literature (pmid INTEGER PRIMARY KEY, title TEXT, year INTEGER)")

    print(f"Parsing {args.filename}...")

    # We need to extract the PMIDs. For fetch_subset, we want first 10 and last 10.
    # To do "last 10" in a streaming parser without storing everything, we can keep a rolling window of the last 10 seen.
    # But for a streaming parser, if we just parse normally, we can extract all to DB and then delete what we don't want.
    # Or keep a list of all PMIDs and then just keep first 10 and last 10.
    # Given we want to be fast and subset should be small, let's just insert all and then delete if subset is true.

    # Actually, inserting all for 30MB gzipped XML (which unzips to 150MB+) is fast enough.

    # Let's parse with lxml
    count = 0
    pmids = []

    with gzip.open(args.filename, 'rb') as f:
        # We only care about PubmedArticle elements
        context = etree.iterparse(f, events=('end',), tag='PubmedArticle')
        for event, elem in context:
            pmid_elem = elem.find('.//PMID')
            title_elem = elem.find('.//ArticleTitle')
            year_elem = elem.find('.//PubDate/Year')

            pmid = int(pmid_elem.text) if pmid_elem is not None and pmid_elem.text else None
            title = title_elem.text if title_elem is not None else ""
            year = int(year_elem.text) if year_elem is not None and year_elem.text else None

            if pmid is not None:
                cursor.execute("INSERT OR IGNORE INTO literature (pmid, title, year) VALUES (?, ?, ?)", (pmid, title, year))
                pmids.append(pmid)
                count += 1

            # Clear the element from memory
            elem.clear()
            # Also eliminate now-empty references from the root node to keep memory low
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    print(f"Inserted {count} records into {db_filename}.")

    if is_subset and len(pmids) > 20:
        print("Subset mode active: keeping only first 10 and last 10 PMIDs.")
        keep_pmids = set(pmids[:10] + pmids[-10:])
        cursor.execute(f"DELETE FROM literature WHERE pmid NOT IN ({','.join('?' for _ in keep_pmids)})", tuple(keep_pmids))
        conn.commit()

    conn.commit()
    conn.close()

    # Remove the xml.gz to save disk space
    os.remove(args.filename)
    print("Done processing chunk.")

if __name__ == "__main__":
    main()
