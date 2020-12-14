import getopt
import json
import os
import subprocess
import sys

import docker

from cdb.api_schema import ApiSchema
from cdb.http import http_get_json, put_payload
from cdb.settings import CDB_SERVER

CMD_HELP = 'ensure_project.py -p <project.json>'
DEFAULT_REPO_ROOT = "/src/"


def load_project_configuration(json_data_file):
    project_data = json.load(json_data_file)
    return project_data


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


"""
Environment parsing
"""


def get_artifact_sha(env=os.environ):
    set_artifact_sha_env_variable_from_file_or_image(env)
    return env.get('CDB_ARTIFACT_SHA', None)


def get_api_token(env=os.environ):
    return env.get('CDB_API_TOKEN', None)


def env_is_compliant():
    return os.getenv('CDB_IS_COMPLIANT', "FALSE") == "TRUE"


def get_host(env=os.environ):
    return env.get('CDB_HOST', CDB_SERVER)


def set_artifact_sha_env_variable_from_file_or_image(env=os.environ):
    """
    This function will update the environment variable CDB_ARTIFACT_SHA.

    If CDB_ARTIFACT_SHA explicitly set no changes will be made.

    If the variable CDB_ARTIFACT_FILENAME is set, CDB_ARTIFACT_SHA will be set to the sha256 digest of the given file.

    if the variable CDB_ARTIFACT_DOCKER_IMAGE is set, CDB_ARTIFACT_SHA will be set to the repoDigest for the image.
    """
    # Only set if not already in environment
    if "CDB_ARTIFACT_SHA" in env:
        return

    artifact_filename = env.get("CDB_ARTIFACT_FILENAME", None)
    artifact_docker_image = env.get("CDB_ARTIFACT_DOCKER_IMAGE", None)

    if artifact_filename is not None:
        print("Getting SHA for artifact: " + artifact_filename)
        artifact_sha = calculate_sha_digest_for_file(artifact_filename)
        print("Calculated digest: " + artifact_sha)
        os.environ["CDB_ARTIFACT_SHA"] = artifact_sha
    elif artifact_docker_image is not None:
        print("Getting SHA for docker image: " + artifact_docker_image)
        artifact_sha = calculate_sha_digest_for_docker_image(artifact_docker_image)
        print("Calculated digest: " + artifact_sha)
        os.environ["CDB_ARTIFACT_SHA"] = artifact_sha
    else:
        raise Exception('Error: One of CDB_ARTIFACT_SHA, CDB_ARTIFACT_FILENAME or CDB_ARTIFACT_DOCKER_IMAGE must be defined')


def calculate_sha_digest_for_file(artifact_filename):
    if not os.path.isfile(artifact_filename):
        raise FileNotFoundError
    output = subprocess.check_output(["openssl", "dgst", "-sha256", artifact_filename])
    digest_in_bytes = output.split()[1]
    artifact_sha = digest_in_bytes.decode('utf-8')
    return artifact_sha


def get_image_details():
    docker_image = os.getenv('CDB_ARTIFACT_DOCKER_IMAGE', "NO_DOCKER_IMAGE_FOUND")
    sha256_digest = os.getenv('CDB_ARTIFACT_SHA', None)
    if sha256_digest is None:
        repo_digest = calculate_sha_digest_for_docker_image(docker_image)
        sha256_digest = repo_digest
    else:
        print("Docker image digest found from environment variable")

    print("IMAGE DIGEST: " + sha256_digest)
    return docker_image, sha256_digest


def calculate_sha_digest_for_docker_image(docker_image):
    client = docker.from_env()
    print("Inspecting docker image for sha256Digest")
    image = client.images.get(docker_image)
    repo_digest = image.attrs["RepoDigests"][0].split(":")[1]
    return repo_digest


def load_user_data():
    """
    Loads user data from the file specified in CDB_USER_DATA
    If CDB_USER_DATA unspecified, returns None
    """
    user_data_file = os.getenv('CDB_USER_DATA', None)
    if user_data_file is None:
        return None
    with open(user_data_file) as file:
        return json.load(file)


def send_evidence(project_file, evidence):
    print(evidence)
    with open(project_file) as project_file_contents:
        _docker_image_unused, sha256_digest = get_image_details()
        api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')
        host = get_host()
        add_evidence(api_token, host, project_file_contents, sha256_digest, evidence)


def add_evidence(api_token, host, project_file_contents, sha256_digest, evidence):
    project_data = load_project_configuration(project_file_contents)
    url = ApiSchema.url_for_artifact(host, project_data, sha256_digest)

    put_payload(evidence, url, api_token)


def build_evidence_dict(is_compliant, evidence_type, description, build_url, user_data=None):
    evidence = {"evidence_type": evidence_type, "contents": {
        "is_compliant": is_compliant,
        "url": "",
        "description": ""
    }}
    if user_data is not None:
        evidence["user_data"]: user_data
    evidence["contents"]["description"] = description
    evidence["contents"]["url"] = build_url
    return evidence


def build_release_json(artifact_sha, description, src_commit_list):
    release_json = {"base_artifact": artifact_sha, "target_artifact": artifact_sha, "description": description,
                    "src_commit_list": src_commit_list}
    return release_json


def build_approval_json(artifact_sha256, description, is_approved, src_commit_list):
    approval_json = {
        "artifact_sha256": artifact_sha256,
        "description": description,
        "is_approved": is_approved,
        "src_commit_list": src_commit_list
    }
    return approval_json


def latest_artifact_for_commit(artifacts_for_commit_response):
    if artifacts_for_commit_response["artifacts"]:
        return artifacts_for_commit_response["artifacts"][-1]["sha256"]
    raise ValueError("No artifact found in ComplianceDB with that SHA")


def get_artifacts_for_commit(host, api_token, project_config_file, commit):
    url = ApiSchema.url_for_commit(host, project_config_file, commit)
    artifact_list = http_get_json(url, api_token)
    return artifact_list

