from cdb.create_deployment import create_deployment

from tests.utils import *

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_create_deployment"


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    # sha provided explicitly
    sha256 = '99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212'
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_ENVIRONMENT": "production",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_deployment("tests/integration/test-pipefile.json")
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

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/deployments/"
    expected_payload = {
        "artifact_sha256": sha256,
        "build_url": None,
        "description": "None",
        "environment": "production"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # mock Docker which calculates the sha
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/runner:4.56",
        "CDB_ENVIRONMENT": "production",
    }
    sha256 = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        create_deployment("tests/integration/test-pipefile.json")
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

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/deployments/"
    expected_payload = {
        "artifact_sha256": sha256,
        "build_url": None,
        "description": "None",
        "environment": "production"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    # Mock openssl which calculates the sha
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_ENVIRONMENT": "production",
    }
    sha256 = "cccdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        create_deployment("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_required_env_vars_uses_CDB_ARTIFACT_FILENAME"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/deployments/"
    expected_payload = {
        "artifact_sha256": sha256,
        "build_url": None,
        "description": "None",
        "environment": "production"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys, mocker):
    # required and optional env-vars
    sha256 = "cccdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    build_url = "https://gitlab/build/1996"
    description = "branch coverage"
    user_data = {"x": 42}
    cdb_env = "production"
    env = {
        "CDB_HOST": "https://app.compliancedb.com",  # optional
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_ENVIRONMENT": cdb_env,
        "CDB_DESCRIPTION": description,  # optional
        "CDB_CI_BUILD_URL": build_url,  # optional
        "CDB_USER_DATA": "/some/file.json"  # optional
    }
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        mocker.patch('cdb.create_deployment.load_user_data', return_value=user_data)
        create_deployment("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars_uses_CDB_ARTIFACT_SHA"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/deployments/"
    expected_payload = {
        "artifact_sha256": sha256,
        "build_url": build_url,
        "description": description,
        "environment": cdb_env,
        "user_data": user_data
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload
