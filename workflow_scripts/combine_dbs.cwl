cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["python3", "combine_dbs.py"]
inputs:
  db_files:
    type: File[]
    inputBinding:
      itemSeparator: " "
      prefix: --db_files
  output_filename:
    type: string?
    default: "combined_catalog.sqlite"
    inputBinding:
      prefix: --output
requirements:
  InitialWorkDirRequirement:
    listing:
      - class: File
        location: combine_dbs.py
outputs:
  combined_db:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)
