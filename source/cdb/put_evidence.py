#!/usr/bin/env python
import os

from cdb.cdb_utils import parse_cmd_line, env_is_compliant, load_user_data, build_evidence_dict, send_evidence


def put_evidence(project_file):
    print("Publish evidence to ComplianceDB")

    is_compliant = env_is_compliant()
    evidence_type = os.getenv('CDB_EVIDENCE_TYPE', "EVIDENCE_TYPE_UNDEFINED")
    description = os.getenv('CDB_DESCRIPTION', "UNDEFINED")
    build_url = os.getenv('CDB_CI_BUILD_URL', "URL_UNDEFINED")
    user_data = load_user_data()

    evidence = build_evidence_dict(is_compliant, evidence_type, description, build_url, user_data)
    send_evidence(project_file, evidence)


if __name__ == '__main__':
    project_file = parse_cmd_line()
    put_evidence(project_file)
