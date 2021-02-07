from cdb.put_evidence import put_evidence

import docker
from pytest import raises
from tests.utils import *

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_put_evidence"

def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # Gets docker daemon to calculates SHA
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    description = "branch coverage"
    build_url = "https://gitlab/build/1956"
    evidence_type = "unit_test"
    env = {
        "CDB_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:4.67",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_DESCRIPTION": description,
        "CDB_CI_BUILD_URL": build_url,
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        put_evidence("tests/integration/test-pipefile.json")
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
            "description": description,
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    # SHA passed in explicitly
    sha256 = "a7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1456"
    evidence_type = "coverage"
    description = "branch coverage"
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_DESCRIPTION": description,
        "CDB_CI_BUILD_URL": build_url,
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
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
            "description": description,
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_both_required_env_vars(capsys):
    # CDB_ARTIFACT_DOCKER_IMAGE is ignored
    build_url = "https://gitlab/build/1456"
    evidence_type = "coverage"
    description = "branch coverage"
    sha256 = "a8cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:4.68",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_DESCRIPTION": description,
        "CDB_CI_BUILD_URL": build_url
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_both_required_env_vars"
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
            "description": description,
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_all_env_vars(capsys):
    # SHA passed in explicitly
    sha256 = "a7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    description = "branch coverage"
    build_url = "https://gitlab/build/1456"
    evidence_type = "coverage"
    env = {
        "CDB_HOST": "https://app.compliancedb.com",  # optional
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_DESCRIPTION": description,
        "CDB_CI_BUILD_URL": build_url,
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
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
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": description,
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_neither_image_nor_sha_env_var_defined_raises_DockerException(capsys):
    env = {
        "CDB_EVIDENCE_TYPE": "test",
        "CDB_DESCRIPTION": "integration test",
        "CDB_CI_BUILD_URL": "integration test",
        "CDB_IS_COMPLIANT": "TRUE",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), \
            raises(docker.errors.DockerException), \
            silent(capsys):
        put_evidence("tests/integration/test-pipefile.json")
