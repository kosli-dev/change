from cdb.put_artifact_image import put_artifact_image
import docker

from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_when_no_env_vars_raises_DockerException():
    """
    This is not the desired behaviour, but until more tests are
    in place we are not refactoring.
    """
    with AutoEnvVars(CDB_DRY_RUN), raises(docker.errors.DockerException):
        put_artifact_image("tests/integration/test-pipefile.json")


def test_when_CDB_ARTIFACT_SHA_is_defined(capsys):
    env = {
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    }

    set_env_vars = {}

    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact_image("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])
