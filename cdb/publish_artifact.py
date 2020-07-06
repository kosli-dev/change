#!/usr/bin/env python

import os

from cdb.cdb_utils import create_artifact, parse_cmd_line, get_image_details, env_is_compliant
from cdb.settings import CDB_SERVER


def main():
    project_file = parse_cmd_line()

    # Get the SHA and Image from string provided in DOCKER_IMAGE
    docker_image, sha256_digest = get_image_details()

    print("Publish artifact to ComplianceDB")
    host = os.getenv('CDB_HOST', CDB_SERVER)

    description = "Created by build " + os.getenv('BUILD_TAG', "UNDEFINED")
    git_commit = os.getenv('GIT_COMMIT', '0000000000000000000000000000000000000000')

    commit_url = os.getenv('GIT_URL', "GIT_URL_UNDEFINED")
    build_url = os.getenv('JOB_DISPLAY_URL', "BUILD_URL_UNDEFINED")
    is_compliant = env_is_compliant()

    print('IS_COMPLIANT: ' + str(is_compliant))

    api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

    with open(project_file) as project_file_contents:
        create_artifact(api_token, host, project_file_contents, sha256_digest, docker_image, description, git_commit,
                        commit_url, build_url, is_compliant)


if __name__ == '__main__':
    main()
