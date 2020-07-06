#!/usr/bin/env python

import os

from cdb.cdb_utils import parse_cmd_line, get_image_details, add_evidence, env_is_compliant
from cdb.settings import CDB_SERVER

DOCKER_IMAGE = "registry.gitlab.com/compliancedb/compliancedb/loancalculator"


def main():
    project_file = parse_cmd_line()

    # Get the SHA and Image from string provided in DOCKER_IMAGE
    docker_image, sha256_digest = get_image_details()

    print("Publish evidence to ComplianceDB")
    host = os.getenv('CDB_HOST', CDB_SERVER)

    is_compliant = env_is_compliant()
    evidence = {"evidence_type": os.getenv('EVIDENCE_TYPE', "EVIDENCE_TYPE_UNDEFINED"), "contents": {
        "is_compliant": is_compliant,
        "url": "",
        "description": ""
    }}
    evidence["contents"]["description"] = os.getenv('CDB_DESCRIPTION', "UNDEFINED")
    evidence["contents"]["url"] = os.getenv('URL', "URL_UNDEFINED")

    api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

    print(evidence)
    with open(project_file) as project_file_contents:
        add_evidence(api_token, host, project_file_contents, sha256_digest, evidence)


if __name__ == '__main__':
    main()
