#!/usr/bin/env python

import os

from cdb.cdb_utils import parse_cmd_line, get_image_details, add_evidence
from cdb.settings import CDB_SERVER

DOCKER_IMAGE = "registry.gitlab.com/compliancedb/compliancedb/loancalculator"


def main():
    project_file = parse_cmd_line()

    print("Get the SHA for the docker image")
    docker_image, sha256_digest = get_image_details()

    print("Publish evidence to ComplianceDB")
    is_compliant = os.getenv('IS_COMPLIANT', "FALSE") == "TRUE"
    evidence = {"evidence_type": os.getenv('EVIDENCE_TYPE', "EVIDENCE_TYPE_UNDEFINED"), "contents": {
        "is_compliant": is_compliant,
        "url": "",
        "description": ""
    }}
    evidence["contents"]["description"] = os.getenv('CDB_DESCRIPTION', "UNDEFINED")
    evidence["contents"]["url"] = os.getenv('URL', "URL_UNDEFINED")
    evidence["contents"]["is_compliant"] = os.getenv('IS_COMPLIANT', "FALSE") == "TRUE"

    api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

    print(evidence)
    with open(project_file) as project_file_contents:
        add_evidence(api_token, CDB_SERVER, project_file_contents, sha256_digest, evidence)


if __name__ == '__main__':
    main()
