import json
import os


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


def build_release_json(artifact_sha, description, src_commit_list):
    release_json = {
        "base_artifact": artifact_sha,
        "target_artifact": artifact_sha,
        "description": description,
         "src_commit_list": src_commit_list
    }
    return release_json


def latest_artifact_for_commit(artifacts_for_commit_response):
    if artifacts_for_commit_response["artifacts"]:
        return artifacts_for_commit_response["artifacts"][-1]["sha256"]
    raise ValueError("No artifact found in ComplianceDB with that SHA")
