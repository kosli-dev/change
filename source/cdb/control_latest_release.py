#!/usr/bin/env python
import sys

from cdb.api_schema import ApiSchema
from cdb.cdb_utils import get_host, get_api_token, get_artifact_sha, parse_cmd_line, load_project_configuration
from cdb.http import http_get_json


def control_latest_release():
    host = get_host()
    api_token = get_api_token()
    artifact_sha = get_artifact_sha()
    project_config_file = parse_cmd_line()

    with open(project_config_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)
        url = ApiSchema.url_for_release(host, project_data, "latest")
        release = http_get_json(url, api_token)

        if release["target_artifact"] != artifact_sha:
            print(f"INCOMPLIANT: latest release {release['release_number']}")
            print(f"    released sha: {release['target_artifact']} ")
            print(f"    expected sha: {artifact_sha} ")
            sys.exit(1)
        else:
            print(f"COMPLIANT: latest release {release['release_number']}")
            print(f"    released sha: {release['target_artifact']} ")
            print(f"    expected sha: {artifact_sha} ")


if __name__ == '__main__':
    control_latest_release()
