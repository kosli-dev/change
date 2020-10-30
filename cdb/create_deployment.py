#!/usr/bin/env python
import os

from cdb.api_schema import ApiSchema
from cdb.cdb_utils import set_artifact_sha_env_variable_from_file_or_image, load_user_data, parse_cmd_line, \
    send_evidence, load_project_configuration, get_host, get_api_token
from cdb.http import http_post_payload


def create_deployment_payload(env=os.environ):
    deployment = {}
    deployment["artifact_sha256"] = env.get('CDB_ARTIFACT_SHA', None)
    deployment["environment"] = env.get('CDB_ENVIRONMENT', None)
    deployment["description"] = env.get('CDB_DESCRIPTION', None)

    if env.get("CDB_USER_DATA"):
        deployment["user_data"] = load_user_data()
    return deployment


def create_deployment(project_file):
    # Todo: make this smoother
    set_artifact_sha_env_variable_from_file_or_image()
    payload = create_deployment_payload()

    with open(project_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)
        url = ApiSchema.url_for_deployments(get_host(), project_data)
        http_post_payload(payload, url, get_api_token())





"""
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA or CDB_ARTIFACT_DOCKER_IMAGE or CDB_ARTIFACT_FILE | Required | The artifact sha that is being deployed |
| CDB_ENVIRONMENT | Required | The environment the artifact is being deployed to |
| CDB_DESCRIPTION | Optional | A description for the deployment |
| CDB_USER_DATA_FILE | Optional | The user data to embed in the deployment, if any (should be mounted in the container) |
"""
if __name__ == '__main__':
    project_file = parse_cmd_line()
    create_deployment(project_file)
