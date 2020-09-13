# ComplianceDB Pipeline Controls

![Continuous Integration Status](https://github.com/compliancedb/cdb_controls/workflows/CI/badge.svg)

This docker image provides some helpers for gathering the audit trail and performing controls in your devops pipelines.

    docker pull compliancedb/cdb_controls
    
## Put project

ComplianceDB has a declarative way to specify the project details.  It is recommended to re-assert the project structure 
on every run of the pipeline.  Since writes are idempotent in ComplianceDB, it will only update if the structure if the 
project changes.  This way, you only need update the `project.json` in your repo and the changes will be reflected in 
ComplianceDB.

Here is an example `project.json`:

```json
{
    "name": "loancalculator",
    "description": "The loan calculator application",
    "owner": "meekrosoft",
    "visibility": "private",
    "template": [
        "artifact",
        "test",
        "coverage",
        "security_scan"
    ]
}
``` 

To put this in the pipeline:
```shell script
docker run --rm --name comply \
        --volume ${PWD}/project.json:/data/project.json \
        --env CDB_HOST=https://app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        compliancedb/cdb_controls python -m cdb.put_project -p /data/project.json
```

This command expect the following environment variables:

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |


## Publish docker image build artifact

To publish a docker build artifact to compliancedb, use the put_artifact_image command.  Note, the command expects
to have access to the docker daemon to query the image details.  This gets the SHA-256 repo digest of the docker image produced.
As such, it should only be called after the image has been pushed to the docker registry.

```shell script
docker run --rm --name comply \
        --volume ${PWD}/project-master.json:/data/project.json \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env CDB_HOST=https://compliancedb-compliancedb-staging.app.compliancedb.com \
        --env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
        --env CDB_ARTIFACT_GIT_URL=${CDB_ARTIFACT_GIT_URL} \
        --env CDB_ARTIFACT_GIT_COMMIT=${CDB_ARTIFACT_GIT_COMMIT} \
        --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
        --env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
        --env CDB_DOCKER_IMAGE=${CDB_DOCKER_IMAGE} \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        compliancedb/cdb_controls python -m cdb.put_artifact_image -p /data/project.json
```

This command expect the following environment variables:

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_IS_COMPLIANT | Required | Whether this artifact is considered compliant from you build process |
| CDB_ARTIFACT_GIT_URL | Required | Link to the source git commit this build was based on |
| CDB_ARTIFACT_GIT_COMMIT | Required | The sha of the git commit that produced this build |
| CDB_CI_BUILD_URL | Required | Link to the build in the ci system |
| CDB_BUILD_NUMBER | Required | Build number |
| CDB_DOCKER_IMAGE | Required | The resulting docker image |


## Publish evidence

To publish a generic evidence type, you can use the `put_evidence` command:
```shell script
docker run --rm --name comply \
        --volume ${PWD}/project-master.json:/data/project.json \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env CDB_HOST=https://compliancedb-compliancedb-staging.app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        --env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
        --env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
        --env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
        --env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
        --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
        --env CDB_DOCKER_IMAGE=${CDB_DOCKER_IMAGE} \
        compliancedb/cdb_controls python -m cdb.put_evidence -p /data/project.json
```

This command expect the following environment variables:

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_IS_COMPLIANT | Required | Whether this artifact is considered compliant from you build process |
| CDB_EVIDENCE_TYPE | Required | The evidence type |
| CDB_DESCRIPTION | Required | The description for the evidence |
| CDB_BUILD_NUMBER | Required | Build number |
| CDB_CI_BUILD_URL | Required | Link to the build information |
| CDB_DOCKER_IMAGE | Required | The docker image that evidence is provided for |


## Control JUnit results

To verify the results a junit test xml, you can use the `control_junit` command.  There are two options for deciding 
the artifact `sha256`: either you can provide it with the `CDB_ARTIFACT_SHA` environment variable, or if this is not 
set the control will try to get it via the docker socket by inspecting the docker image given with `CDB_DOCKER_IMAGE`.

```shell script
docker run --rm --name comply \
        --volume ${PWD}/${PROJFILE}:/data/project.json \
        --volume ${PWD}/tmp/coverage/htmlcov/junit.xml:/data/junit/junit.xml \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env CDB_HOST=https://app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        --env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
        --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
        --env CDB_DOCKER_IMAGE=${CDB_DOCKER_IMAGE} \
        ${IMAGE} python -m cdb.control_junit -p /data/project.json
```


| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_EVIDENCE_TYPE | Required | The evidence type for the results |
| CDB_CI_BUILD_URL | Required | The URL to link to from ComplianceDB |
| CDB_ARTIFACT_SHA or CDB_DOCKER_IMAGE | Required | The artifact sha to report this evidence against |

## Create a release

To create a release in ComplianceDB, you can use the `create_release` command

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA | Optional | The SHA256 for the artifact that you would like to release, if not given then this is retrieved from CDB  |
| CDB_TARGET_SRC_COMMITISH | Required | The source commit-ish for the oldest change in the release |
| CDB_BASE_SRC_COMMITISH | Required | The source commit-ish for the oldest change in the release |
| CDB_RELEASE_DESCRIPTION | Optional | A description of the release |
| CDB_SRC_REPO_ROOT | Optional | The path where the source git repository is mounted, default to `/src` |
