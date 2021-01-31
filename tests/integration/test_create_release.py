from cdb.create_release import create_release

from tests.utils import ScopedEnvVars, ScopedDirCopier, CDB_DRY_RUN, verify_approval
from tests.unit.test_git import TEST_REPO_ROOT
import pytest

def test_required_env_vars_and_CDB_ARTIFACT_SHA_is_none(capsys, mocker):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"}]
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}), ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.create_release.get_artifact_sha', return_value=None)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_only_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    sha = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": sha}]
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/runner:4.56",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {"CDB_ARTIFACT_SHA": sha}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_only_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    sha = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": sha}]
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {"CDB_ARTIFACT_SHA": sha}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",  # optional
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_RELEASE_DESCRIPTION": "Description",  # optional
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,  # optional
    }
    set_env_vars = {}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

def test_required_env_vars_and_SHA_cannot_be_calculated(capsys):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}), ScopedDirCopier("/test_src", "/src"), pytest.raises(Exception) as excinfo:
        create_release("tests/integration/test-pipefile.json")
    assert "Error: One of CDB_ARTIFACT_SHA, CDB_ARTIFACT_FILENAME or CDB_ARTIFACT_DOCKER_IMAGE must be defined" == str(excinfo.value)