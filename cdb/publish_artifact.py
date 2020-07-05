#!/usr/bin/env python

import os

from cdb.cdb_utils import create_artifact, parse_cmd_line, get_image_details
from cdb.settings import CDB_SERVER


def main():
    project_file = parse_cmd_line()

    print("Get the SHA for the docker image")
    docker_image, sha256_digest = get_image_details()

    print("Publish to ComplianceDB")
    description = "Created by build " + os.getenv('BUILD_TAG', "UNDEFINED")
    git_commit = os.getenv('GIT_COMMIT', '0000000000000000000000000000000000000000')

    commit_url = os.getenv('GIT_URL', "GIT_URL_UNDEFINED")
    build_url = os.getenv('JOB_DISPLAY_URL', "BUILD_URL_UNDEFINED")
    print(os.getenv('IS_COMPLIANT', "FALSE"))
    is_compliant = os.getenv('IS_COMPLIANT', "FALSE") == "TRUE"

    api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

    with open(project_file) as project_file_contents:
        create_artifact(api_token, CDB_SERVER, project_file_contents, sha256_digest, docker_image, description, git_commit,
                        commit_url, build_url, is_compliant)


if __name__ == '__main__':
    main()
