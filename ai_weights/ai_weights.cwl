cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["python3", "generate_db.py"]
inputs:
  fetch_subset:
    type: boolean?
    inputBinding:
      prefix: --fetch_subset
  data_source:
    type: string?
    inputBinding:
      prefix: --data_source
requirements:
  InitialWorkDirRequirement:
    listing:
      - class: File
        location: generate_db.py
outputs:
  db_out:
    type: File
    outputBinding:
      glob: "ai_weights.sqlite"
