requirements:
  MultipleInputFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}
cwlVersion: v1.2
class: Workflow

inputs:
  fetch_subset:
    type: boolean?
    default: true
  data_source:
    type: string?
    default: "zenodo"

steps:
  ai_weights_step:
    run: ai_weights/ai_weights.cwl
    in:
      fetch_subset: fetch_subset
      data_source: data_source
    out: [db_out]

  cohorts_step:
    run: cohorts/cohorts.cwl
    in:
      fetch_subset: fetch_subset
      data_source: data_source
    out: [db_out]

  tools_materials_step:
    run: tools_materials/tools_materials.cwl
    in:
      fetch_subset: fetch_subset
      data_source: data_source
    out: [db_out]

  literature_step:
    run: literature/literature.cwl
    in:
      fetch_subset: fetch_subset
      data_source: data_source
    out: [db_out]

  combine_step:
    run: workflow_scripts/combine_dbs.cwl
    in:
      db_files:
        - ai_weights_step/db_out
        - cohorts_step/db_out
        - tools_materials_step/db_out
        - literature_step/db_out
    out: [combined_db]

outputs:
  final_catalog_db:
    type: File
    outputSource: combine_step/combined_db
