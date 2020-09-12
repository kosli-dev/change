import getopt
import json
import os
import sys
import docker
import requests as req
from junitparser import JUnitXml
from pygit2 import Repository, _pygit2
from pygit2._pygit2 import GIT_SORT_TIME
from requests.auth import HTTPBasicAuth

from cdb.settings import CDB_SERVER

CMD_HELP = 'ensure_project.py -p <project.json>'
DEFAULT_REPO_ROOT = "/src/"


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


def http_get_json(url, api_token):
    print("Getting this endpoint: " + url)
    resp = req.get(url, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)
    return resp.json()


def put_payload(payload, url, api_token):
    headers = {"Content-Type": "application/json"}
    print("Putting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    resp = req.put(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)


def post_payload(payload, url, api_token):
    headers = {"Content-Type": "application/json"}
    print("Putting this payload:")
    print(json.dumps(payload, sort_keys=True, indent=4))
    print("To url: " + url)
    resp = req.post(url, data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(api_token, 'unused'))
    print(resp.text)


def url_for_artifacts(host, project_data):
    return url_for_project(host, project_data) + '/artifacts/'


def add_evidence(api_token, host, project_file_contents, sha256_digest, evidence):
    project_data = load_project_configuration(project_file_contents)
    url = url_for_artifact(host, project_data, sha256_digest)

    put_payload(evidence, url, api_token)


def url_for_artifact(host, project_data, sha256_digest):
    return url_for_artifacts(host, project_data) + sha256_digest


def url_for_project(host, project_data):
    return host + '/api/v1/projects/' + project_data["owner"] + '/' + project_data["name"]


def url_for_artifacts(host, project_data):
    return url_for_project(host, project_data) + '/artifacts/'


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

    print("IMAGE DIGEST: " + sha256_digest)
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
        host = get_host()
        add_evidence(api_token, host, project_file_contents, sha256_digest, evidence)


def get_host():
    return os.getenv('CDB_HOST', CDB_SERVER)


def build_evidence_dict(is_compliant, evidence_type, description, build_url):
    evidence = {"evidence_type": evidence_type, "contents": {
        "is_compliant": is_compliant,
        "url": "",
        "description": ""
    }}
    evidence["contents"]["description"] = description
    evidence["contents"]["url"] = build_url
    return evidence


def commit_for_commitish(repo, commitish):
    """returns the commit for a given reference as a string"""
    commit = repo.revparse_single(commitish)
    return str(commit.id)


def list_commits_between(repo, target_commit, base_commit):
    start = repo.revparse_single(target_commit)
    stop = repo.revparse_single(base_commit)

    commits = []

    walker = repo.walk(start.id, GIT_SORT_TIME)
    walker.hide(stop.id)
    for commit in walker:
        commits.append(str(commit.id))

    return commits


def repo_at(root):
    try:
        repo = Repository(root + '.git')
    except _pygit2.GitError:
        return None
    return repo


def build_release_json(artifact_sha, description, src_commit_list):
    json = {}
    json["base_artifact"] = artifact_sha
    json["target_artifact"] = artifact_sha
    json["description"] = description
    json["src_commit_list"] = src_commit_list
    return json


def latest_artifact_for_commit(artifacts_for_commit_response):
    return artifacts_for_commit_response["artifacts"][-1]["sha256"]


def create_release_environment_variables():
    env = {
        "host": get_host(),
        "base_src_commit": os.getenv('CDB_BASE_SRC_COMMITISH', None),
        "target_src_commit": os.getenv('CDB_TARGET_SRC_COMMITISH', None),
        "artifact_sha": os.getenv('CDB_ARTIFACT_SHA', None),
        "api_token": os.getenv('CDB_API_TOKEN', None),
        "description": os.getenv('CDB_RELEASE_DESCRIPTION', "No description provided"),
        "repo_path": os.getenv('CDB_SRC_REPO_ROOT', DEFAULT_REPO_ROOT)
    }
    return env


def get_artifacts_for_commit(host, api_token, project_config_file, commit):
    url = url_for_commit(host, project_config_file, commit)
    artifact_list = http_get_json(url, api_token)
    return artifact_list


def create_release():
    project_config_file = parse_cmd_line()
    env = create_release_environment_variables()
    with open(project_config_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)

        if env["artifact_sha"] is None:
            src_commit = commit_for_commitish(repo_at(env["repo_path"]), env["target_src_commit"])
            response = get_artifacts_for_commit(env["host"], env["api_token"], project_data, src_commit)
            env["artifact_sha"] = latest_artifact_for_commit(response)
            print(f"Found artifact {env['artifact_sha']} as latest artifact for source commit {env['target_src_commit']}")

        commit_list = list_commits_between(repo_at(env["repo_path"]), env["target_src_commit"], env["base_src_commit"])
        release_json = build_release_json(env["artifact_sha"], env["description"], commit_list)
        url = url_for_releases(env["host"], project_data)
        post_payload(release_json, url, env["api_token"])


def url_for_releases(host, project_data):
    return url_for_project(host, project_data) + '/releases/'


def url_for_commit(host, project_data, commit):
    return url_for_project(host, project_data) + '/commits/' + commit
