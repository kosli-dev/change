from pathlib import Path

from cdb.git import repo_at, list_commits_between

TEST_REPO_ROOT = "/test_src/"

"""
We have a test repo with a commit graph like this:

    * e0d1acf1adb9e263c1b6e0cfe3e0d2c1ade371e1 2020-09-12 (HEAD -> release-branch)  Initial approval commit (Mike Long)
    * 8f5b384644eb83e7f2a6d9499539a077e7256b8b 2020-09-12 (master)  Fourth commit (Mike Long)
    * e0ad84e1a2464a9486e777c1ecde162edff930a9 2020-09-12  Third commit (Mike Long)
    * b6c9e60f281e37d912ec24f038b7937f79723fb4 2020-09-12 (production)  Second commit (Mike Long)
    * b7e6aa63087fcb1e64a5f2a99c8d255415d8cb99 2020-09-12  Initial commit (Mike Long)
    
This repo is added in the docker image at /test_src/

"""


def test_repo_is_present_in_image():
    repo_path = Path("/test_src/.git")
    assert repo_path.is_dir()


def test_is_repo():
    assert repo_at(TEST_REPO_ROOT) is not None
    assert repo_at("/cdb_data/") is None


def test_list_commits_between_master_and_production():
    commits = list_commits_between(repo_at(TEST_REPO_ROOT), target_commit="master", base_commit="production")
    expected = [
        "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
        "e0ad84e1a2464a9486e777c1ecde162edff930a9"]
    assert commits == expected


def test_list_commits_between_approval_branch_and_production():
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
