from cdb.put_artifact_image import put_artifact_image
import docker

from pytest import raises
from tests.utils import *


APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_put_artifact_image"


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # artifact sha calculated from CDB_ARTIFACT_DOCKER_IMAGE

    sha256 = "ddcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ee"
    commit = "12037940e4e7503055d8a8eea87e177f04f14616"
    artifact_name = "acme/widget:3.4"

    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": artifact_name,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": f"http://github/me/project/commit/{commit}",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": "BUILD_URL_UNDEFINED",
        "commit_url": f"http://github/me/project/commit/{commit}",
        "description": "Created by build UNDEFINED",
        "filename": artifact_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys, mocker):
    # artifact sha comes direct from CDB_ARTIFACT_SHA
    commit = "92037940e4e7503055d8a8eea87e177f04f14616"
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": f"http://github/me/project/commit/{commit}",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_required_env_vars_uses_CDB_ARTIFACT_SHA"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": "BUILD_URL_UNDEFINED",
        "commit_url": f"http://github/me/project/commit/{commit}",
        "description": "Created by build UNDEFINED",
        "filename": "NO_DOCKER_IMAGE_FOUND",
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

def test_all_env_vars(capsys):
    # artifact sha comes direct from CDB_ARTIFACT_SHA
    build_url = "https://gitlab/build/351"
    commit = "82037940e4e7503055d8a8eea87e177f04f14616"
    sha256="b7cdaef69c676c2466571d9933380d559ccc2032b258fc5e73f99a103db462ef"
    env = {
        "CDB_HOST": "https://app.compliancedb.com",  # optional
        "CDB_API_TOKEN": "6599831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": f"http://github/me/project/commit/{commit}",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
        "CDB_CI_BUILD_URL": build_url,  # optional
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": f"http://github/me/project/commit/{commit}",
        "description": "Created by build UNDEFINED",
        "filename": "NO_DOCKER_IMAGE_FOUND",
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_no_env_vars_raises_DockerException():
    """
    This is not the desired behaviour, but until more tests are
    in place we are not refactoring.
    """
    set_env_vars = {}

    with ScopedEnvVars(CDB_DRY_RUN, set_env_vars), raises(docker.errors.DockerException):
        put_artifact_image("tests/integration/test-pipefile.json")


