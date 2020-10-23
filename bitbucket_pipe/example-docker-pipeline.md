# Examples for file artifacts

Here are some pipeline examples fro tracking file-base artifacts 
## Put Pipeline
```yaml
        script:
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: pipeline-def.json
              CDB_COMMAND: 'put_pipeline'
              CDB_API_TOKEN: $CDB_API_TOKEN
```

## Put Artifact

The artifact sha256 is automatically calculated from the artifact file.

```yaml
        script:
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: pipeline-def.json
              CDB_COMMAND: 'put_artifact'
              CDB_API_TOKEN: $CDB_API_TOKEN
              CDB_IS_COMPLIANT: "TRUE"
              CDB_ARTIFACT_DOCKER_IMAGE: compliancedb/helloworld
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
              CDB_PIPELINE_DEFINITION: pipeline-def.json
              CDB_COMMAND: 'control_junit'
              CDB_API_TOKEN: $CDB_API_TOKEN
              CDB_TEST_RESULTS_DIR: "/data/junit"
              CDB_EVIDENCE_TYPE: "pytest_test_results"
              CDB_ARTIFACT_FILENAME: "artifact.txt"
              CDB_DESCRIPTION: "Tests passed"
````

## Create release

```yaml
    - step:
        name: Make release in ComplianceDB
        trigger: manual
        script:
          - git branch -av
          - git fetch origin "+refs/heads/*:refs/remotes/origin/*"
          - git branch -av
          - pipe: docker://compliancedb/cdb_controls-bbpipe:latest
            variables:
              CDB_PIPELINE_DEFINITION: pipeline.json
              CDB_COMMAND: 'create_release'
              CDB_API_TOKEN: $CDB_API_TOKEN
              CDB_ARTIFACT_FILENAME: "artifact.txt"
              CDB_RELEASE_DESCRIPTION: "Release created in pipeline"
              CDB_TARGET_SRC_COMMITISH: master
              CDB_BASE_SRC_COMMITISH: origin/production
```