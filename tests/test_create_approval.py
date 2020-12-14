
"""
We have a test repo with a commit graph like this:

    * e0d1acf1adb9e263c1b6e0cfe3e0d2c1ade371e1 2020-09-12 (HEAD -> approval-branch)  Initial approval commit (Mike Long)
    * 8f5b384644eb83e7f2a6d9499539a077e7256b8b 2020-09-12 (master)  Fourth commit (Mike Long)
    * e0ad84e1a2464a9486e777c1ecde162edff930a9 2020-09-12  Third commit (Mike Long)
    * b6c9e60f281e37d912ec24f038b7937f79723fb4 2020-09-12 (production)  Second commit (Mike Long)
    * b7e6aa63087fcb1e64a5f2a99c8d255415d8cb99 2020-09-12  Initial commit (Mike Long)

Get the artifact SHA from CDB using latest policy
Get the list of commits
Create the JSON
Put the JSON

"""
from pathlib import Path
import pytest

from cdb.cdb_utils import build_release_json, latest_artifact_for_commit, build_approval_json
from cdb.create_approval import create_approval_environment_variables
from cdb.git import list_commits_between, repo_at
from cdb.api_schema import ApiSchema


def test_url_for_approvals():
    partial_project_data = {"name": "hadroncollider", "owner": "cern"}
    url = ApiSchema.url_for_approvals(host="http://localhost", project_data=partial_project_data)
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/approvals/"


def test_create_approval_base_payload():
    env = {
        "CDB_HOST": "private.compliancedb.com",
        "CDB_API_TOKEN": "somesupersecretvalue",
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": "/some/directory"
    }
    env_vars = create_approval_environment_variables(env)

    assert env_vars == {
        "host": env["CDB_HOST"],
        "api_token": env["CDB_API_TOKEN"],
        "artifact_sha256": "1234",
        'base_src_commit': "production",
        "target_src_commit": "master",
        "description": "Description",
        "is_externally_approved": False,
        "repo_path": "/some/directory",
    }


def test_create_approval_dict():
    artifact_sha256 = "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c23"
    src_commit_list = [
        "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
        "e0ad84e1a2464a9486e777c1ecde162edff930a9"]
    description = "Approval description text"
    is_approved = False

    expected = {
        "artifact_sha256":  artifact_sha256,
        "description": description,
        "is_approved": is_approved,
        "src_commit_list": src_commit_list,
    }

    actual = build_approval_json(
        artifact_sha256=artifact_sha256, description=description, is_approved=is_approved, src_commit_list=src_commit_list)
    assert expected == actual

#
# def test_parse_artifact_by_commit():
#     """
#     Retrieve a list of artifacts registered against a given commit.
#
#     GET
#     'http://localhost/api/v1/projects/test/hadroncollider/commits/e412ad6f7ea530ee9b83df964a0dde2b477be720'
#
#     RESPONSE
#     {
#         "artifacts": [
#             {
#                 "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0"
#             },
#             {
#                 "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c20"
#             }
#         ]
#     }
#     """
#
#     api_response = {
#             "artifacts": [
#                 {
#                     "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0"
#                 },
#                 {
#                     "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c20"
#                 }
#             ]
#         }
#
#     assert latest_artifact_for_commit(api_response) == "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c20"
#
#
# def test_parse_artifact_by_commit_when_no_artifacts_raises_error():
#     api_response = {
#         "artifacts": []
#     }
#     with pytest.raises(ValueError):
#         latest_artifact_for_commit(api_response)
#
#
# def test_url_for_approvals():
#     partial_project_data = {"name": "hadroncollider", "owner": "cern"}
#     url = ApiSchema.url_for_approvals(host="http://localhost", project_data=partial_project_data)
#     assert url == "http://localhost/api/v1/projects/cern/hadroncollider/approvals/"
#
#
# def test_url_for_commit():
#     partial_project_data = {"name": "hadroncollider", "owner": "cern"}
#     url = ApiSchema.url_for_commit(host="http://localhost", project_data=partial_project_data, commit="12345678")
#     assert url == "http://localhost/api/v1/projects/cern/hadroncollider/commits/12345678"
