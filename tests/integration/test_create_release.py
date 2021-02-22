from cdb.create_release import create_release

from tests.utils import *
from tests.unit.test_git import TEST_REPO_ROOT
import pytest

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_create_release"

def test_required_env_vars_and_CDB_ARTIFACT_SHA_is_none(capsys, mocker):
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": sha256}]
    }

    with dry_run(env), ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.create_release.get_artifact_sha', return_value=None)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_required_env_vars_and_CDB_ARTIFACT_SHA_is_none"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/releases/"
    expected_payload = {
        "base_artifact": sha256,
        "description": "No description provided",
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
        "target_artifact": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_only_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": sha256}]
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/runner:4.56",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {"CDB_ARTIFACT_SHA": sha256}
    with dry_run(env, set_env_vars), ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_only_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/releases/"
    expected_payload = {
        "base_artifact": sha256,
        "description": "No description provided",
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
        "target_artifact": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_only_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": sha256}]
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }
    set_env_vars = {"CDB_ARTIFACT_SHA": sha256}
    with dry_run(env, set_env_vars), ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_only_required_env_vars_uses_CDB_ARTIFACT_FILENAME"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/releases/"
    expected_payload = {
        "base_artifact": sha256,
        "description": "No description provided",
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
        "target_artifact": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    description = "Description"
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,  # optional
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_RELEASE_DESCRIPTION": description,  # optional
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,  # optional
    }
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        create_release("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars_uses_CDB_ARTIFACT_SHA"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "test.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Posting"
    expected_url = f"http://{domain}/api/v1/projects/{owner}/{name}/releases/"
    expected_payload = {
        "base_artifact": sha256,
        "description": description,
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
        "target_artifact": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_and_SHA_cannot_be_calculated(capsys):
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
    }

    with dry_run(env), ScopedDirCopier("/test_src", "/src"), pytest.raises(Exception) as excinfo:
        create_release("tests/integration/test-pipefile.json")
    assert "Error: One of CDB_ARTIFACT_SHA, CDB_ARTIFACT_FILENAME or CDB_ARTIFACT_DOCKER_IMAGE must be defined" == str(excinfo.value)