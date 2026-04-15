cwlVersion: v1.2
class: Workflow
requirements:
  ScatterFeatureRequirement: {}
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}

inputs:
  fetch_subset:
    type: boolean?
    default: true
  data_source:
    type: string?

steps:
  setup_jobs_step:
    run: setup_jobs.cwl
    in:
      fetch_subset: fetch_subset
    out: [jobs_json]

  parse_jobs_step:
    run:
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}
      inputs:
        jobs_file: File
      outputs:
        urls: string[]
        md5s: string[]
        filenames: string[]
      expression: |
        ${
          var jobs = JSON.parse(inputs.jobs_file.contents);
          var urls = [];
          var md5s = [];
          var filenames = [];
          for (var i = 0; i < jobs.length; i++) {
            urls.push(jobs[i].url);
            md5s.push(jobs[i].md5);
            filenames.push(jobs[i].filename);
          }
          return { "urls": urls, "md5s": md5s, "filenames": filenames };
        }
    in:
      jobs_file:
        source: setup_jobs_step/jobs_json
        loadContents: true
    out: [urls, md5s, filenames]

  process_chunk_step:
    run: process_chunk.cwl
    scatter: [url, md5, filename]
    scatterMethod: dotproduct
    in:
      url: parse_jobs_step/urls
      md5: parse_jobs_step/md5s
      filename: parse_jobs_step/filenames
      fetch_subset: fetch_subset
    out: [chunk_db]

  qc_and_combine_step:
    run: qc_and_combine.cwl
    in:
      db_files: process_chunk_step/chunk_db
      fetch_subset: fetch_subset
    out: [combined_db, qc_report]

outputs:
  db_out:
    type: File
    outputSource: qc_and_combine_step/combined_db
  qc_report_out:
    type: File
    outputSource: qc_and_combine_step/qc_report
