from cdb.create_approval import create_approval

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval
from tests.unit.test_git import TEST_REPO_ROOT
import os
from distutils.dir_util import copy_tree, remove_tree


def test_only_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    # Mock openssl which calculates the sha
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "ttcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), DirManager("/test_src","/src"):
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])

''' Need to be fixed: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0).
Maybe to use mocker.patch('cdb.cdb_utils.get_artifacts_for_commit',)
def test_only_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # mock Docker which calculates the sha
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/runner:4.56",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    sha = "444daef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), DirManager("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])


def test_only_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    sha = "444daef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), DirManager("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out", "err"])
'''

def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "ttcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_DESCRIPTION": "Description", #optional
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE", #optional
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT, #optional
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])


class DirManager(object):
    def __init__(self, source_dir, target_dir):
        self._source_dir = source_dir
        self._target_dir = target_dir

    def __enter__(self):
        os.mkdir(self._target_dir)
        copy_tree(self._source_dir, self._target_dir)

    def __exit__(self, _type, _value, _traceback):
        remove_tree(self._target_dir)
