from cdb.control_junit import control_junit
import docker
import requests
from pytest import raises
from tests.utils import *

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_control_junit"


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1456"
    evidence_type = "unit_test"
    env = {
        "CDB_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url,
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}):
        control_junit("tests/integration/test-pipefile.json")
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
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"
    env = {
        "CDB_API_TOKEN": "7199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:3.4",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url
    }
    set_env_vars = {}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        sha256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        control_junit("tests/integration/test-pipefile.json")
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
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_uses_non_existent_CDB_TEST_RESULTS_DIR(capsys, mocker):
    # Uses CDB_TEST_RESULTS_DIR == /does/not/exist
    # which is not checked. Results in message
    # "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites"
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    env = {
        "CDB_HOST": "https://app.compliancedb.com",
        "CDB_API_TOKEN": "7199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_TEST_RESULTS_DIR": "/does/not/exist",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url
    }
    set_env_vars = {}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_uses_non_existent_CDB_TEST_RESULTS_DIR"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_uses_existing_CDB_TEST_RESULTS_DIR_with_failing_xml(capsys):
    # Uses CDB_TEST_RESULTS_DIR == /app/tests/data/control_junit/xml-with-fails
    # which exists. Results in message
    # "JUnit results xml verified by compliancedb/cdb_controls: Tests contain failures"
    build_url = "https://gitlab/build/217"
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    evidence_type = "coverage"
    env = {
        "CDB_HOST": "https://app.compliancedb.com",
        "CDB_API_TOKEN": "7100831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_TEST_RESULTS_DIR": "/app/tests/data/control_junit/xml-with-fails",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url,
    }
    set_env_vars = {}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_uses_existing_CDB_TEST_RESULTS_DIR_with_failing_xml"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: Tests contain failures",
            "is_compliant": False,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_uses_existing_CDB_TEST_RESULTS_DIR_with_error_xml(capsys):
    # Uses CDB_TEST_RESULTS_DIR == /app/tests/data/control_junit/xml-with-error
    # which exists. Results in message
    # "JUnit results xml verified by compliancedb/cdb_controls: Tests contain errors"
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/217"
    evidence_type = "coverage"
    env = {
        "CDB_HOST": "https://app.compliancedb.com",
        "CDB_API_TOKEN": "7100831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_TEST_RESULTS_DIR": "/app/tests/data/control_junit/xml-with-error",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url
    }
    set_env_vars = {}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_uses_existing_CDB_TEST_RESULTS_DIR_with_error_xml"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: Tests contain errors",
            "is_compliant": False,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_uses_existing_CDB_TEST_RESULTS_DIR_with_passing_xml(capsys, mocker):
    # Uses all optional env vars
    # Uses CDB_TEST_RESULTS_DIR == /app/tests/data/control_junit/xml-with-passed-results
    # which exists. Results in message
    # "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 2 test suites"
    build_url = "https://gitlab/build/217"
    evidence_type = "coverage"
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    user_data = {"username": "test_user"}
    env = {
        "CDB_HOST": "https://app.compliancedb.com",
        "CDB_API_TOKEN": "7100831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_TEST_RESULTS_DIR": "/app/tests/data/control_junit/xml-with-passed-results",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url,
        "CDB_USER_DATA": "/some/file.json"  # optional
    }
    set_env_vars = {}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.control_junit.load_user_data', return_value=user_data)
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_uses_existing_CDB_TEST_RESULTS_DIR_with_passing_xml"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 2 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type,
        "user_data": user_data
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_no_env_vars_raises_DockerException(capsys):
    env = CDB_DRY_RUN
    set_env_vars = {}
    with ScopedEnvVars(env, set_env_vars), silent(capsys), \
            raises((docker.errors.DockerException, requests.exceptions.ConnectionError)):
        control_junit("tests/integration/test-pipefile.json")
