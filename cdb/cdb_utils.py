import getopt
import json
import os
import sys
import docker
import requests as req
from junitparser import JUnitXml
from requests.auth import HTTPBasicAuth

from cdb.settings import CDB_SERVER

CMD_HELP = 'ensure_project.py -p <project.json>'


def project_exists_in_cdb(project_data, projects):
    exists = False
    for project in projects:
        if project["name"] == project_data["name"]:
            exists = True
    return exists


def get_project_list_from_cdb(projects_url):
    resp = req.get(projects_url)
    # If the response was successful, no Exception will be raised
    resp.raise_for_status()
    print(resp.text)
    projects = resp.json()
    return projects


def get_project_from_cdb(project_url):
    resp = req.get(project_url)
    # If the response was successful, no Exception will be raised
    resp.raise_for_status()
    print(resp.text)
    project = resp.json()
    return project


def load_project_configuration(json_data_file):
    project_data = json.load(json_data_file)
    return project_data


def create_artifact(api_token, host, project_config_file, sha256, filename, description, git_commit, commit_url, build_url,
                    is_compliant):
    project_data = load_project_configuration(project_config_file)

    '''
    curl -H 'Content-Type: application/json' \
     -X PUT \
     -d '{"sha256": "'"$3"'", "filename": "'"$4"'", "description": "'"$5"'", "git_commit": "'"$6"'", "commit_url": "'"$7"'", "build_url": "'"$8"'", "is_compliant": "true"}' \
    http://server:8001/api/v1/projects/$1/$2/artifacts/
    '''

    create_artifact_payload = {
        "sha256": sha256,
        "filename": filename,
        "description": description,
        "git_commit": git_commit,
        "commit_url": commit_url,
        "build_url": build_url,
        "is_compliant": is_compliant
    }
    url = url_for_artifacts(host, project_data)
    put_payload(create_artifact_payload, url, api_token)


def put_payload(payload, url, api_token):
    headers = {"Content-Type": "application/json"}
    print("Putting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    resp = req.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)


def url_for_artifacts(host, project_data):
    return url_for_project(host, project_data) + project_data["name"] + '/artifacts/'


def add_evidence(api_token, host, project_file_contents, sha256_digest, evidence):
    project_data = load_project_configuration(project_file_contents)
    url_for_artifact = url_for_artifacts(host, project_data) + sha256_digest

    put_payload(evidence, url_for_artifact, api_token)


def url_for_project(host, project_data):
    return host + '/api/v1/projects/' + project_data["owner"] + '/'


def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring


def parse_cmd_line():
    project_file = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["project="])
    except getopt.GetoptError:
        print(CMD_HELP)
        sys.exit(2)
    for opt, arg in opts:
        print(opt + ": " + arg)
        if opt == '-h':
            print(CMD_HELP)
            sys.exit()
        elif opt in ("-p", "--project"):
            project_file = arg
    return project_file


def get_image_details():
    docker_image = os.getenv('CDB_DOCKER_IMAGE', "NO_DOCKER_IMAGE_FOUND")
    sha256_digest = os.getenv('CDB_ARTIFACT_SHA', None)
    if sha256_digest is None:
        client = docker.from_env()
        print("Inspecting docker image for sha256Digest")
        image = client.images.get(docker_image)
        sha256_digest = image.attrs["RepoDigests"][0].split(":")[1]
    else:
        print("Docker image digest found from environment variable")

    print("IMAGE DIGEST: " + str(image.attrs["RepoDigests"][0]))
    return docker_image, sha256_digest


def env_is_compliant():
    return os.getenv('CDB_IS_COMPLIANT', "FALSE") == "TRUE"


def is_compliant_suite(junit_xml):
    if junit_xml.failures != 0:
        return False, "Tests contain failures"
    if junit_xml.errors != 0:
        return False, "Tests contain errors"
    return True, "All tests passed"


def load_test_results(file_path):
    test_xml = JUnitXml.fromfile(file_path)
    return test_xml


def is_compliant_test_results(file_path):
    """
    This parses a junit xml file to determine if there are any errors or failures

    return:
        A tuple, with is_compliant, plus a message string
    """
    test_xml = load_test_results(file_path)
    if test_xml._tag == "testsuites":
        for suite in test_xml:
            suite_is_compliant, message = is_compliant_suite(suite)
            if not suite_is_compliant:
                return suite_is_compliant, message
        # every test suite passed, so return True
        return True, "All tests passed"
    if test_xml._tag == "testsuite":
        return is_compliant_suite(test_xml)
    return False, "Could not find test suite(s)"


def control_junit():
    print("Publish evidence to ComplianceDB")
    junit_results_path = "/data/junit/junit.xml"

    is_compliant, message = is_compliant_test_results(junit_results_path)
    evidence_type = os.getenv('CDB_EVIDENCE_TYPE', "junit")
    description = "JUnit results xml verified by compliancedb/cdb_controls: " + message
    build_url = os.getenv('CDB_CI_BUILD_URL', "URL_UNDEFINED")

    evidence = build_evidence_dict(is_compliant, evidence_type, description, build_url)
    send_evidence(evidence)


def put_evidence():
    print("Publish evidence to ComplianceDB")

    is_compliant = env_is_compliant()
    evidence_type = os.getenv('CDB_EVIDENCE_TYPE', "EVIDENCE_TYPE_UNDEFINED")
    description = os.getenv('CDB_DESCRIPTION', "UNDEFINED")
    build_url = os.getenv('CDB_CI_BUILD_URL', "URL_UNDEFINED")

    evidence = build_evidence_dict(is_compliant, evidence_type, description, build_url)
    send_evidence(evidence)


def send_evidence(evidence):
    print(evidence)
    project_file = parse_cmd_line()
    with open(project_file) as project_file_contents:
        _docker_image_unused, sha256_digest = get_image_details()
        api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')
        host = os.getenv('CDB_HOST', CDB_SERVER)
        add_evidence(api_token, host, project_file_contents, sha256_digest, evidence)


def build_evidence_dict(is_compliant, evidence_type, description, build_url):
    evidence = {"evidence_type": evidence_type, "contents": {
        "is_compliant": is_compliant,
        "url": "",
        "description": ""
    }}
    evidence["contents"]["description"] = description
    evidence["contents"]["url"] = build_url
    return evidence
