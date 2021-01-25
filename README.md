# ComplianceDB Pipeline Controls

![Continuous Integration Status](https://github.com/compliancedb/cdb_controls/workflows/CI/badge.svg)

This docker image provides some helpers for gathering the audit trail and performing controls in your devops pipelines.

    docker pull compliancedb/cdb_controls
    
## Put pipeline

ComplianceDB has a declarative way to specify the pipeline details.  It is recommended to re-assert the pipeline structure 
on every run of the pipeline.  Since writes are idempotent in ComplianceDB, it will only update if there is a change
 to the pipeline.  This way, you only need update the `pipeline.json` in your repo and the changes will be reflected in 
ComplianceDB.

Here is an example `pipeline.json`:

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
        --volume ${PWD}/pipeline.json:/data/pipeline.json \
        --env CDB_HOST=https://app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        compliancedb/cdb_controls python -m cdb.put_pipeline -p /data/pipeline.json
```

This command expect the following environment variables:

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |

## Publish file-based build artifact

This command creates an artifact in compliancedb based on a file.

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_FILENAME | Required | The artifact filename |
| CDB_ARTIFACT_SHA | Optional | The SHA256 for the artifact |
| CDB_IS_COMPLIANT | Required | Whether this artifact is considered compliant from you build process |
| CDB_ARTIFACT_GIT_URL | Required | Link to the source git commit this build was based on |
| CDB_ARTIFACT_GIT_COMMIT | Required | The sha of the git commit that produced this build |
| CDB_CI_BUILD_URL | Required | Link to the build in the ci system |
| CDB_BUILD_NUMBER | Required | Build number |

If you use a `CDB_ARTIFACT_FILENAME` to specify the artifact, you must mount it into the container so the openssl 
digest can be calculated.  Alternatively, you can specify directly by setting the `CDB_ARTIFACT_SHA` variable.

```shell script
docker run --rm --name comply \
 			--volume ${PWD}/${PROJFILE}:/data/project.json \
			--volume=/var/run/docker.sock:/var/run/docker.sock \
			--volume=${PWD}/Dockerfile:/data/artifact.txt \
			--env CDB_HOST=${CDB_HOST} \
			--env CDB_API_TOKEN="${CDB_API_TOKEN}" \
			--env CDB_IS_COMPLIANT="TRUE" \
			--env CDB_ARTIFACT_GIT_URL="http://github/me/project/commits/3451345234523453245" \
			--env CDB_ARTIFACT_GIT_COMMIT="134125123541234123513425" \
			--env CDB_CI_BUILD_URL="https://gitlab/build/1234" \
			--env CDB_BUILD_NUMBER="1234" \
			--env CDB_ARTIFACT_FILENAME=/data/artifact.txt \
	        ${IMAGE} python -m cdb.put_artifact -p /data/project.json
```

## Publish docker image build artifact

To publish a docker build artifact to compliancedb, use the put_artifact_image command.  Note, the command expects
to have access to the docker daemon to query the image details.  This gets the SHA-256 repo digest of the docker image produced.
As such, it should only be called after the image has been pushed to the docker registry.

```shell script
docker run --rm --name comply \
        --volume ${PWD}/pipeline-master.json:/data/pipeline.json \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env CDB_HOST=https://compliancedb-compliancedb-staging.app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        --env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
        --env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
        --env CDB_ARTIFACT_GIT_URL=${CDB_ARTIFACT_GIT_URL} \
        --env CDB_ARTIFACT_GIT_COMMIT=${CDB_ARTIFACT_GIT_COMMIT} \
        --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
        compliancedb/cdb_controls python -m cdb.put_artifact_image -p /data/pipeline.json
```

This command expect the following environment variables:

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_DOCKER_IMAGE | Required | The resulting docker image |
| CDB_IS_COMPLIANT | Required | Whether this artifact is considered compliant from you build process |
| CDB_ARTIFACT_GIT_URL | Required | Link to the source git commit this build was based on |
| CDB_ARTIFACT_GIT_COMMIT | Required | The sha of the git commit that produced this build |
| CDB_CI_BUILD_URL | Required | Link to the build in the ci system |


## Publish generic evidence

To publish a generic evidence type, you can use the `put_evidence` command:
```shell script
docker run --rm --name comply \
        --volume ${PWD}/pipeline-master.json:/data/pipeline.json \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env CDB_HOST=https://compliancedb-compliancedb-staging.app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        --env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
        --env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
        --env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
        --env CDB_DESCRIPTION="${CDB_DESCRIPTION}" \
        --env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
        --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
        compliancedb/cdb_controls python -m cdb.put_evidence -p /data/pipeline.json
```

This command expect the following environment variables:

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_DOCKER_IMAGE | Required | The docker image that evidence is provided for |
| CDB_IS_COMPLIANT | Required | Whether this artifact is considered compliant from you build process |
| CDB_EVIDENCE_TYPE | Required | The evidence type |
| CDB_DESCRIPTION | Required | The description for the evidence |
| CDB_BUILD_NUMBER | Required | Build number |
| CDB_CI_BUILD_URL | Required | Link to the build information |


## Control JUnit results

To verify the results a junit test xml, you can use the `control_junit` command.  There are two options for deciding 
the artifact `sha256`: either you can provide it with the `CDB_ARTIFACT_SHA` environment variable, or if this is not 
set the control will try to get it via the docker socket by inspecting the docker image given with `CDB_ARTIFACT_DOCKER_IMAGE`.

```shell script
docker run --rm --name comply \
        --volume ${PWD}/${PROJFILE}:/data/pipeline.json \
        --volume ${PWD}/tmp/coverage/htmlcov/junit.xml:/data/junit/junit.xml \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --env CDB_HOST=https://app.compliancedb.com \
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        --env CDB_ARTIFACT_DOCKER_IMAGE=${CDB_ARTIFACT_DOCKER_IMAGE} \
        --env CDB_EVIDENCE_TYPE=${CDB_EVIDENCE_TYPE} \
        --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
        ${IMAGE} python -m cdb.control_junit -p /data/pipeline.json
```


| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA or CDB_ARTIFACT_DOCKER_IMAGE | Required | The artifact sha to report this evidence against |
| CDB_TEST_RESULTS_DIR | Optional | Location of junit xml result files. Defaults to `/data/junit/` |
| CDB_EVIDENCE_TYPE | Required | The evidence type for the results |
| CDB_CI_BUILD_URL | Required | The URL to link to from ComplianceDB |

## Create an approval with a git history

To create an approval in ComplianceDB, you can use the `create_approval` command

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA or CDB_ARTIFACT_DOCKER_IMAGE | Optional | The SHA256 for the artifact that you would like to approve, if not given then this is retrieved from CDB  |
| CDB_BASE_SRC_COMMITISH | Required | The source commit-ish for the oldest change in the approval |
| CDB_TARGET_SRC_COMMITISH | Required | The source commit-ish for the oldest change in the approval |
| CDB_DESCRIPTION | Optional | A description for the approval |
| CDB_IS_APPROVED_EXTERNALLY | Optional | Use this if the approval has taken place outside compliancedb, default false |
| CDB_SRC_REPO_ROOT | Optional | The path where the source git repository is mounted, default to `/src` |


## Create a deployment

To create a deployment in ComplianceDB, you can use the `create_deployment` command.  You can optionally provide a 
json file with user_data if required.


```shell script
echo "{'url':'https:'https://gitlab.com/compliancedb/compliancedb/-/jobs/785151532'}" > tmp/deployment_user_data.json
docker run --rm --name comply \
        --volume ${PWD}/${PIPELINEFILE}:/data/pipeline.json \
        --volume ${PWD}/tmp/deployment_user_data.json:/data/deployment_user_data.json \
        --volume=/var/run/docker.sock:/var/run/docker.sock \		
        --env CDB_API_TOKEN=${CDB_API_TOKEN} \
        --env CDB_ARTIFACT_SHA=${CDB_ARTIFACT_SHA} \
        --env CDB_ENVIRONMENT=production \
        --env CDB_CI_BUILD_URL=${CI_BUILD_URL} \
        --env CDB_DESCRIPTION="Deployed to production in pipeline" \
        --env USER_DATA_FILE=/data/pipeline.json \
        ${IMAGE} python -m cdb.create_deployment -p /data/pipeline.json
```

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA or CDB_ARTIFACT_DOCKER_IMAGE or CDB_ARTIFACT_FILE | Required | The artifact sha that is being deployed |
| CDB_ENVIRONMENT | Required | The environment the artifact is being deployed to |
| CDB_DESCRIPTION | Optional | A description for the deployment |
| CDB_CI_BUILD_URL | Optional | A url for the deployment |
| CDB_USER_DATA_FILE | Optional | The user data to embed in the deployment, if any (should be mounted in the container) |

## Control that an artifact is latest released

To control that a given artifact is the latest release ComplianceDB, you can use the `control_latest_release` command

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA | Required | The SHA256 for the artifact  |

This will return a non-zero exit code in case of no release found.


## Record Bitbucket pull request approval state

To publish the bitbucket pull request information this artifact comes from, use the `put_bitbucket_pr` command.

| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA | Required | The SHA256 for the artifact  |
| BITBUCKET_WORKSPACE | Required | The bitbucket workspace this repo is in |
| BITBUCKET_REPO_SLUG | Required | The bitbucket repo slug |
| BITBUCKET_COMMIT | Required | The bitbucket commit |
| BITBUCKET_USER | Required | The username to authenticate with |
| BITBUCKET_PWD | Required | The app password to authenticate with |
