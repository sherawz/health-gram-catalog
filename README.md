# health-gram-catalog
A multi-agent + multi-human AI experiment to build and maintain a catalog of the world's biomedical knowledge.

the catalog will have four sections:
* AI Weights
* well-consented human cohorts
* tools and materials
* literature

We should write a cwl workflow that downloads a subset of metadata for each section. It could accept some parameters to download more (or all) data or to fetch the data from Zenodo or an Arvados instance managed by the Pwrsonal Genome Project informatics initiative. 

Once the data subset is downloaded rhe workflow should process each section, in parallel, into a sqlite database, do some QC / generate some summary stats for the section and, in a final step, combine the individual sqlite databases into a single database. 

We may want to add indexes so we can browse the combined sqlite database in a javascript metadata browser using a library that supports partial reads. 

Finally we ahould make a demo video about the overall project. Lets plan to have a series of videos as we make progress on rhe project. 

For concreteness, let's use arvados-tools and save each workflow step in zenodo. 

In the future we can fetch the data from Zenodo or Arvadoa to guarantee reproducibility and not re-mirror external resourcss while we are iterating.  

we should find a way for multiple human/agent workers to work on the project, simultaneously. 
