# Tools & Materials

This directory handles the metadata processing for Tools and Materials within the Health Gram Catalog.

**Goal**: Fetch, parse, and process metadata for tools/materials and store it into an SQLite database.

We are going to make a catalog of bioinformatics tools and any associated human materials such tools require for validation and benchmarking. 

To get started we can focus on Bioconda & Biocontainers + materials shared by the Harvard Personal Genome Project at Coriell.

Rough outline:

(1)  Replicate Bioconda and Biocontainers infrastructure alongside the prefix.dev toolchain (pixi, rattler, rattler-build) to mirror, resolve dependencies, and build recipes from source on-demand.

(2) Investigate orchestrating the entire mirroring and build pipeline using Common Workflow Language (CWL), including integrating tools like mulled-build for on-the-fly container generation.

(3) Push and store the built container images within an Arvados instance maintained by the Personal Genome Project, including handling alternative storage backends if needed.

(4) Save metadata in a SQLite database, including storing pointers, cryptographic hashes to containers themselves.

(5) Identify and integrate open-source container and source code scanning tools (e.g., Syft for SBOMs, Trivy/Grype for vulnerabilities) into the CWL workflow to scan artifacts automatically post-build.

(6) Define a periodic update strategy for the SQLite database, including implementing Quality Control (QC) checks and lightweight statistical scripts to validate the integrity of the catalog.

(7) Formulate a process for packaging and depositing stable, QC-passed versions of the SQLite metadata catalog into Zenodo for long-term archiving and citation.

(8) Review community terms of service and API rate limits to explicitly define "good citizen" rules (e.g., exponential backoff, off-peak polling) to avoid straining upstream Prefix / Bioconda/ Biocontainers infrastructure.


**Collaboration**: The Tools & Materials team will work within this directory to write their specific `CommandLineTool` definitions and scripts.
