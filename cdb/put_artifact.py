#!/usr/bin/env python

import os

from cdb.cdb_utils import create_artifact, parse_cmd_line, get_image_details, env_is_compliant
from cdb.settings import CDB_SERVER


def main():
    project_file = parse_cmd_line()

    # Get the SHA and Filename from string provided in CDB_DOCKER_IMAGE
    filename = os.getenv('CDB_ARTIFACT_FILENAME', "UNDEFINED")
    if filename == "UNDEFINED":
        print("Cannot find CDB_ARTIFACT_FILENAME in the environment variables")
        return

    sha256_digest = os.getenv('CDB_ARTIFACT_SHA', "UNDEFINED")
    if sha256_digest == "UNDEFINED":
        print("Cannot find CDB_ARTIFACT_SHA in the environment variables")
        return

    print("Publish artifact to ComplianceDB")
    host = os.getenv('CDB_HOST', CDB_SERVER)

    description = "Created by build " + os.getenv('CDB_BUILD_NUMBER', "UNDEFINED")
    git_commit = os.getenv('CDB_ARTIFACT_GIT_COMMIT', '0000000000000000000000000000000000000000')

    commit_url = os.getenv('CDB_ARTIFACT_GIT_URL', "GIT_URL_UNDEFINED")
    build_url = os.getenv('CDB_CI_BUILD_URL', "BUILD_URL_UNDEFINED")
    is_compliant = env_is_compliant()

    print('CDB_IS_COMPLIANT: ' + str(is_compliant))

    api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

    with open(project_file) as project_file_contents:
        create_artifact(api_token, host, project_file_contents, sha256_digest, filename, description, git_commit,
                        commit_url, build_url, is_compliant)


if __name__ == '__main__':
    main()
