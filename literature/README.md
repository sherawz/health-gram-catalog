# Literature

This directory handles the metadata processing for Literature within the Health Gram Catalog.

**Goal**: Fetch, parse, and process metadata for literature and store it into an SQLite database.
**Collaboration**: The Literature team works within this directory to orchestrate workflows (`.cwl`) and Python scripts to robustly handle parsing the massive dataset of biomedical publications.

## PubMed Baseline Processing Architecture

This directory uses a Common Workflow Language (CWL) workflow (`literature.cwl`) that runs sub-steps to process the NCBI PubMed baseline:

1. **Discovery**: A script scans the NCBI PubMed baseline directory (`https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/`) and collects URLs for `.xml.gz` files and their corresponding MD5 hashes.
2. **Parallel Download and Processing**: Using CWL's `Scatter` feature, the workflow processes each chunk in parallel:
   - Downloads the `.xml.gz` chunk.
   - Verifies the downloaded file matches the NCBI provided MD5 hash.
   - Uses `lxml.etree.iterparse` to rapidly parse the XML stream (which is very fast and uses minimal memory).
   - Extracts key metadata (PMID, title, year) and writes it into a chunk-specific SQLite database.
3. **QC & Combination**: Once all chunks are downloaded and processed, a final step runs:
   - Downloads the Europe PMC index mapping (`PMID_PMCID_DOI.csv.gz`).
   - Cross-references PMIDs found in our SQLite databases against the PMIDs available in Europe PMC to ensure we have complete metadata coverage. It generates a QC report.
   - Combines the individual chunk SQLite databases into the final `literature.sqlite` database.

## Zenodo Subset Mode (`fetch_subset`)

Because the entire PubMed baseline is several hundred gigabytes, it cannot easily be deposited into Zenodo or used for rapid testing/reproducibility workflows.

To support this, the workflow accepts a boolean parameter `--fetch_subset`. When `true`, the workflow acts as follows:
- We extract only the **first 10** and **last 10** PMIDs from each XML chunk.
- We filter the Europe PMC index down to only those same IDs.

This results in a relatively small but highly representative SQLite database and QC report that can be quickly executed, tested, and distributed via Zenodo, proving that the workflow operates completely correctly for any baseline version.

## Execution

The `literature.cwl` workflow is designed to be executed as part of the overarching `main.cwl` at the root of the project. However, you can run it independently:

```bash
# Run with subset enabled (fast)
cwltool literature.cwl --fetch_subset true

# Run against full dataset (slow, requires massive disk space)
cwltool literature.cwl --fetch_subset false
```

### Dependencies

To run the custom python scripts within the CWL workflow, we utilize:
- Standard python library `sqlite3` for DB creation.
- Standard python library `hashlib` for MD5 verification.
- `requests` for fetching remote files.
- `lxml` for fast XML parsing.
