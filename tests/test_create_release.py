
"""
We have a test repo with a commit graph like this:

    * e0d1acf (HEAD -> release-branch) Initial release commit
    * 8f5b384 (master) Fourth commit
    * e0ad84e Third commit
    * b6c9e60 (production) Second commit
    * b7e6aa6 Initial commit

Get the artifact SHA from CDB using latest policy
Get the list of commits
Create the JSON
Put the JSON

"""
from pathlib import Path

from pygit2 import Repository, _pygit2

REPO_ROOT = "/test_src/"


def test_repo_is_present_in_image():
    repo_path = Path("/test_src/.git")
    assert repo_path.is_dir()


def is_repo(root):
    try:
        repo = Repository(root + '.git')
    except _pygit2.GitError:
        return False
    return True


def test_is_repo():
    assert is_repo(REPO_ROOT)
    assert not is_repo("/cdb_data/")

