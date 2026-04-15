cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["python3", "setup_jobs.py"]
requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - class: File
        location: setup_jobs.py
inputs:
  fetch_subset:
    type: boolean?
    inputBinding:
      prefix: --fetch_subset
      valueFrom: '$(self ? "true" : "false")'
outputs:
  jobs_json:
    type: File
    outputBinding:
      glob: "jobs.json"
