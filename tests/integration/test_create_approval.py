from cdb.create_approval import create_approval

from tests.utils import AutoEnvVars, AutoDirCopier, CDB_DRY_RUN, verify_approval
from tests.unit.test_git import TEST_REPO_ROOT


def test_only_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "ttcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), AutoDirCopier("/test_src", "/src"):
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])


def test_only_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    sha = "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0"
    mock_artifacts_for_commit ={
        "artifacts": [ {"sha256": sha} ]
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/runner:4.56",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), AutoDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        mocker.patch('cdb.create_approval.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])


def test_only_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    sha = "084c799cd551dd1d8d5c5f9a5d593b2e931f5e36122ee5c793c1d08a19839cc0"
    mock_artifacts_for_commit = {
        "artifacts": [ {"sha256": sha} ]
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), AutoDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        mocker.patch('cdb.create_approval.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "ttcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_DESCRIPTION": "Description",  # optional
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",  # optional
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,  # optional
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_approval("tests/integration/test-pipefile.json", env)
    verify_approval(capsys, ["out"])
