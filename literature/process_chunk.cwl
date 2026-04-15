cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["python3", "process_chunk.py"]
requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - class: File
        location: process_chunk.py
inputs:
  url:
    type: string
    inputBinding:
      prefix: --url
  md5:
    type: string
    inputBinding:
      prefix: --md5
  filename:
    type: string
    inputBinding:
      prefix: --filename
  fetch_subset:
    type: boolean?
    inputBinding:
      prefix: --fetch_subset
      valueFrom: '$(self ? "true" : "false")'
outputs:
  chunk_db:
    type: File
    outputBinding:
      glob: "*.sqlite"
