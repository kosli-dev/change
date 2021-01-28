from cdb.put_evidence import put_evidence

import docker
from pytest import raises
from tests.utils import ScopedEnvVars, CDB_DRY_RUN, verify_approval, auto_reading


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # Gets docker daemon to calculates SHA
    env = {
        "CDB_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:4.67",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "unit_test",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1956",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        sha = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        put_evidence("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    # SHA passed in explicitly
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "a7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "coverage",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_both_required_env_vars(capsys):
    # CDB_ARTIFACT_DOCKER_IMAGE is ignored
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:4.68",
        "CDB_ARTIFACT_SHA": "a8cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "coverage",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_all_env_vars(capsys):
    # SHA passed in explicitly
    env = {
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "a7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "coverage",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


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
            auto_reading(capsys):
        put_evidence("tests/integration/test-pipefile.json")
