# Personal Genome Project initiative (PGPi) Health Gram Catalog
A multi-agent + multi-human AI experiment to build and maintain a catalog of the world's biomedical knowledge. 
 
The catalog is divided into four sections, each managed by dedicated teams working in their respective subdirectories:

* [**AI Weights**](ai_weights/README.md)
* [**Well-consented human cohorts**](cohorts/README.md)
* [**Tools and materials**](tools_materials/README.md)
* [**Literature**](literature/README.md)

Additionally, the [**Health Gram Explorer**](health-gram-explorer/README.md) team is building a stand-alone, interactive health gram catalog metadata explorer that runs from your web-browser. 

Released editions of the (possibly abbreviated) catalog will be publicly available at Zenodo.  Full versions of the catalog will be available via health grams obtained from the Personal Genome Project informatics (PGPi) initiative.    

We plan to release the catalog twice a year. It will be available on one or more bootable microSDs — in a few editions — to suit different needs and budgets. If we limit ourselves to a catalog that weighs less than a gram, that's about three microSDs of catalog data (~4.5-6TB) and weighs ~900miligrams. A PGPi health gram (or PGPi h-gram) is a physical, unique instantiation of a specific, versioned edition of the health gram catalog as well as network access credentials and all associated software.   Anyone can help curate — or contribute to — the health gram catalog by sending pull requests on GitHub.  If you only plan to use the metadata catalog, there is no need to get a health-gram or access the PGPi network.   Although anyone can contribute, priority will be given to individuals who deploy the PGPi health gram catalog and contribute physical hardware to the Personal Genome Project informatics network. 

Collectively, local computers booting from health-gram microSDs will create a private networked environment to do useful bioinformatics, explore Personal Genome Project data, and grow the world's biomedical knowledge.  

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

Finally we should make a demo video about the overall project. Let's plan to have a series of blog posts, presentations and video demos as we make progress on the project.
