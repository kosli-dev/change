# Bitbucket Pipe for ComplianceDB Controls

This pipe provides a simple way to integrate with ComplianceDB.  Ou 

## Put Pipeline
```yaml
        script:
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: $BITBUCKET_CLONE_DIR/pipe.json
              CDB_COMMAND: 'put_pipeline'
              CDB_API_TOKEN: $CDB_API_TOKEN
```

# Put Artifact

```yaml
        script:
          - ls -al
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: $BITBUCKET_CLONE_DIR/pipe.json
              CDB_COMMAND: 'put_artifact'
              CDB_API_TOKEN: $CDB_API_TOKEN
              CDB_IS_COMPLIANT: "TRUE"
              CDB_ARTIFACT_FILENAME: "artifact.txt"
```