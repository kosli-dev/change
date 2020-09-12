
"""
We have a test repo with a commit graph like this:

    * e0d1acf1adb9e263c1b6e0cfe3e0d2c1ade371e1 2020-09-12 (HEAD -> release-branch)  Initial release commit (Mike Long)
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

from cdb.cdb_utils import list_commits_between, \
    repo_at, build_release_json, latest_artifact_for_commit, url_for_releases, url_for_commit

TEST_REPO_ROOT = "/test_src/"


def test_repo_is_present_in_image():
    repo_path = Path("/test_src/.git")
    assert repo_path.is_dir()


def test_is_repo():
    assert repo_at(TEST_REPO_ROOT) is not None
    assert repo_at("/cdb_data/") is None


def test_list_commits_between_master_and_production():
    commits = list_commits_between(repo_at(TEST_REPO_ROOT), "master", "production")
    expected = [
        "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
        "e0ad84e1a2464a9486e777c1ecde162edff930a9"]
    assert commits == expected


def test_list_commits_between_release_branch_and_production():
    commits = list_commits_between(repo_at(TEST_REPO_ROOT), "release-branch", "master")
    expected = [
        "e0d1acf1adb9e263c1b6e0cfe3e0d2c1ade371e1"]
    assert commits == expected


def test_list_commits_between_master_and_commit():
    commits = list_commits_between(repo_at(TEST_REPO_ROOT), "master", "b7e6aa63087fcb1e64a5f2a99c8d255415d8cb99")
    expected = [
        "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
        "e0ad84e1a2464a9486e777c1ecde162edff930a9",
        "b6c9e60f281e37d912ec24f038b7937f79723fb4"
    ]
    assert commits == expected


def test_create_release_dict():
    artifact_sha = "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c23"
    description = "Release description text"
    src_commit_list = [
        "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
        "e0ad84e1a2464a9486e777c1ecde162edff930a9"]

    expected = {
        "base_artifact":  artifact_sha,
        "target_artifact": artifact_sha,
        "description": description,
        "src_commit_list": src_commit_list
    }

    actual = build_release_json(artifact_sha, description, src_commit_list)
    assert expected == actual


def test_parse_artifact_by_commit():
    """
    Retrieve a list of artifacts registered against a given commit.

    GET
    'http://localhost/api/v1/projects/test/hadroncollider/commits/e412ad6f7ea530ee9b83df964a0dde2b477be720'

    RESPONSE
    {
        "artifacts": [
            {
                "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0"
            },
            {
                "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c20"
            }
        ]
    }
    """

    api_response = {
            "artifacts": [
                {
                    "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0"
                },
                {
                    "sha256": "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c20"
                }
            ]
        }

    assert latest_artifact_for_commit(api_response) == "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839c20"


def test_url_for_releases():
    partial_project_data = {"name": "hadroncollider", "owner": "cern"}
    url = url_for_releases(host="http://localhost", project_data=partial_project_data)
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/releases/"


def test_url_for_commit():
    partial_project_data = {"name": "hadroncollider", "owner": "cern"}
    url = url_for_commit(host="http://localhost", project_data=partial_project_data, commit="12345678")
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/commits/12345678"
