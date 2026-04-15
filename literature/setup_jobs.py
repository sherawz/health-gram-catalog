import argparse
import requests
import re
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Discover PubMed Baseline URLs and MD5 hashes")
    # cwl passes --fetch_subset with "true" or "false" if we use boolean input but we can also handle missing
    parser.add_argument("--fetch_subset", type=str, choices=["true", "false", ""], nargs="?", const="true", default="false", help="If true, only fetch a few chunks for testing.")
    args = parser.parse_args()

    is_subset = args.fetch_subset.lower() == "true"

    base_url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch baseline directory: {e}")
        sys.exit(1)

    html = response.text
    gz_files = re.findall(r'href="(pubmed\d{2}n\d{4}\.xml\.gz)"', html)
    gz_files = sorted(list(set(gz_files)))

    if is_subset:
        gz_files = gz_files[:2]

    jobs = []
    for gz in gz_files:
        md5_url = base_url + gz + ".md5"
        try:
            md5_response = requests.get(md5_url, timeout=30)
            md5_response.raise_for_status()
            content = md5_response.text.strip()
            # Content looks like: MD5(pubmed26n0001.xml.gz)= fb7c05737f47f7e07245f0c064c6e00a
            md5_hash = content.split("=")[-1].strip()

            jobs.append({
                "url": base_url + gz,
                "md5": md5_hash,
                "filename": gz
            })
        except Exception as e:
            print(f"Failed to fetch md5 for {gz}: {e}")
            continue

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    main()
