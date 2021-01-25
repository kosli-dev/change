from cdb.control_junit import control_junit
import docker
from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_EVIDENCE_TYPE": "unit_test",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_no_env_vars():
    env = CDB_DRY_RUN
    set_env_vars = {}
    with AutoEnvVars(env, set_env_vars), raises(docker.errors.DockerException):
        control_junit("tests/integration/test-pipefile.json")



