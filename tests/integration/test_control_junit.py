from cdb.control_junit import control_junit
import docker
from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_message_when_no_env_vars(capsys):
    env = CDB_DRY_RUN
    set_env_vars = {}
    with AutoEnvVars(env, set_env_vars), raises(docker.errors.DockerException):
        control_junit("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])


def test_message_when_CDB_TEST_RESULTS_DIR_defined(capsys):
    env = {"CDB_TEST_RESULTS_DIR": "tests/integration/"}
    set_env_vars = {}

    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), raises(docker.errors.DockerException):
        control_junit("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])
