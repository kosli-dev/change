# Examples for file artifacts

Here are some pipeline examples fro tracking file-base artifacts 
## Put Pipeline
```yaml
        script:
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: $BITBUCKET_CLONE_DIR/pipe.json
              CDB_COMMAND: 'put_pipeline'
              CDB_API_TOKEN: $CDB_API_TOKEN
```

## Put Artifact

The artifact sha256 is automatically calculated from the artifact file.

```yaml
        script:
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: $BITBUCKET_CLONE_DIR/pipe.json
              CDB_COMMAND: 'put_artifact'
              CDB_API_TOKEN: $CDB_API_TOKEN
              CDB_IS_COMPLIANT: "TRUE"
              CDB_ARTIFACT_FILENAME: "artifact.txt"
```

## Control junit

````yaml
    - step:
        name: Control junit results and publish to ComplianceDB
        script:
          - mkdir -p /data/junit
          - cp test_results.xml /data/junit
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: $BITBUCKET_CLONE_DIR/pipeline.json
              CDB_COMMAND: 'control_junit'
              CDB_API_TOKEN: $CDB_API_TOKEN
              CDB_TEST_RESULTS_DIR: "/data/junit"
              CDB_EVIDENCE_TYPE: "pytest_test_results"
              CDB_ARTIFACT_FILENAME: "artifact.txt"
              CDB_DESCRIPTION: "Tests passed"
````