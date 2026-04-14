# Collaboration Guide

Welcome to the `health-gram-catalog` project! This project aims to build a comprehensive, multi-agent + multi-human AI maintained catalog of the world's biomedical knowledge. Due to the massive scale of the data and the parallel nature of our workflows, we have structured the project to allow multiple teams (composed of human and AI agent pairs) to work simultaneously without stepping on each other's toes.

## Division of Labor

The project is naturally divided into distinct sections. Each team will take ownership of a specific directory and its corresponding data pipelines:

1. **AI Weights Team (`ai_weights/`)**: Responsible for gathering metadata about open biomedical AI models, processing it, and saving it into a SQLite database.
2. **Cohorts Team (`cohorts/`)**: Responsible for curating metadata for well-consented human cohorts and formatting it into SQLite.
3. **Tools & Materials Team (`tools_materials/`)**: Responsible for tools, lab materials, and related entities.
4. **Literature Team (`literature/`)**: Responsible for scientific literature metadata.
5. **Explorer Team (`health-gram-explorer/`)**: Responsible for building the JavaScript metadata browser using a library that supports partial reads of SQLite databases (e.g., HTTP VFS via range requests) to prevent loading massive databases into RAM.
6. **Integration / Lead Team**: Oversees the root CWL workflow (`main.cwl`) and the scripts that combine individual databases into the final master catalog database.

## Technical Infrastructure

To ensure smooth collaboration, we rely on the following technical strategies:

### 1. Version Control & Branching
- **Isolation by Directory**: Each team primarily works within their designated folder. This minimizes merge conflicts in Git.
- **Feature Branches**: All work should be done on feature branches (e.g., `feature/literature-metadata-fetch`) and submitted as Pull Requests (PRs).
- **Review Process**: Human and agent teams should review each other's PRs to ensure quality and compliance with the overall project schema.

### 2. Common Workflow Language (CWL)
- **Modularity**: The main pipeline is written in CWL (`main.cwl` in the root directory). Teams should build their sub-workflows and tools within their directories and export CWL `CommandLineTool` definitions that the main workflow can call.
- **Reproducibility**: CWL guarantees that data processing steps are reproducible across environments. We execute our CWL workflows using `arvados-tools`.

### 3. Data Management
- **Arvados**: The primary data management system for large datasets. Intermediate artifacts, final multi-hundred gigabyte SQLite databases, and workflow steps should be shared via Arvados projects. This prevents duplication of external resources during iteration.
- **Zenodo**: Used for smaller, representative data subsets that exercise the majority of functionality. This is highly useful for CI/CD, testing, and debugging without needing to download massive datasets. The `main.cwl` workflow accepts a parameter to toggle fetching from Zenodo versus Arvados.

## Getting Started for Teams

1. Clone the repository.
2. Read the `README.md` in your designated folder to understand the specific scope of your section.
3. Use `arvados-tools` locally with a small data subset (or stub data) to test your scripts.
4. Ensure your script outputs a correctly formatted SQLite database.
5. Update your section's CWL tool definition to wrap your script.
6. Run the master `main.cwl` from the root directory to verify that your component successfully integrates with the rest of the project.
