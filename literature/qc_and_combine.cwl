cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["python3", "qc_and_combine.py"]
requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - class: File
        location: qc_and_combine.py
      - $(inputs.db_files)
inputs:
  db_files:
    type: File[]
  fetch_subset:
    type: boolean?
    inputBinding:
      prefix: --fetch_subset
      valueFrom: '$(self ? "true" : "false")'
outputs:
  combined_db:
    type: File
    outputBinding:
      glob: "literature.sqlite"
  qc_report:
    type: File
    outputBinding:
      glob: "qc_report.txt"
