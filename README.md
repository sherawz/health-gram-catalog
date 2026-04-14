# health-gram-catalog
A multi-agent + multi-human AI experiment to build and maintain a catalog of the world's biomedical knowledge.

We are collecting the world's biomedical knowledge in a physical gram. We plan to distribute versioned libraries of the catalog on collections of bootable microSDs.

## Project Structure

The catalog is divided into four sections, each managed by dedicated teams working in their respective subdirectories:

* [**AI Weights**](ai_weights/README.md)
* [**Well-consented human cohorts**](cohorts/README.md)
* [**Tools and materials**](tools_materials/README.md)
* [**Literature**](literature/README.md)

Additionally, the [**Health Gram Explorer**](health-gram-explorer/README.md) team is building a Javascript interactive metadata explorer utilizing partial-reads (HTTP VFS) so large SQLite databases don't have to be fully loaded into memory.

For details on how multiple teams of human/agent pairs collaborate across these sections without conflicts, see our [**Collaboration Guide**](collaboration.md).

## Workflow Execution

We have written a CWL workflow (`main.cwl`) that downloads metadata for each section. It accepts parameters like `fetch_subset` to download more (or all) data and `data_source` to fetch the data from Zenodo or an Arvados instance managed by the Personal Genome Project informatics initiative.

When executed, the workflow processes each section in parallel into a SQLite database, generating summary stats, and in a final step, combines the individual SQLite databases into a single database.

For concreteness, let's use `arvados-cwl-runner` and save each workflow step in Zenodo.

### Installation & Execution

To run the workflow locally, install `arvados-tools` which provides a drop-in replacement for the standard CWL runner:

```bash
# Install arvados-cwl-runner
pip install arvados-cwl-runner

# Run the master workflow locally
arvados-cwl-runner main.cwl --fetch_subset true --data_source zenodo
```

In the future we can fetch the data from Zenodo or Arvados to guarantee reproducibility and not re-mirror external resources while we are iterating. SQLite databases could be several hundred gigabytes so won't fit in Zenodo, but we can construct subsets that exercise a majority of functionality.

## Roadmap

Finally we should make a demo video about the overall project. Let's plan to have a series of videos as we make progress on the project.
