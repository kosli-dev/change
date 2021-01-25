from cdb.control_junit import control_junit
import docker
from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_no_env_vars():
    env = CDB_DRY_RUN
    set_env_vars = {}
    with AutoEnvVars(env, set_env_vars), raises(docker.errors.DockerException):
        control_junit("tests/integration/test-pipefile.json")



