from cdb.put_evidence import put_evidence

import docker
from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval, auto_reading


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "a7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "coverage",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_BUILD_NUMBER": "19",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_evidence("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_when_no_env_vars_raises_DockerException(capsys):
    set_env_vars = {}
    with AutoEnvVars(CDB_DRY_RUN, set_env_vars), \
            raises(docker.errors.DockerException), \
            auto_reading(capsys):
        put_evidence("tests/integration/test-pipefile.json")


def test_when_neither_image_nor_sha_env_var_defined_raises_DockerException(capsys):
    env = {
        "CDB_EVIDENCE_TYPE": "test",
        "CDB_DESCRIPTION": "integration test",
        "CDB_CI_BUILD_URL": "integration test",
        "CDB_IS_COMPLIANT": "TRUE",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), \
            raises(docker.errors.DockerException), \
            auto_reading(capsys):
        put_evidence("tests/integration/test-pipefile.json")
