from cdb.put_artifact_image import put_artifact_image
import docker

from pytest import raises
from tests.utils import AutoEnvVars, cdb_dry_run


def test_when_no_env_vars_raises_DockerException():
    """
    This is not the desired behaviour, but until more tests are
    in place we are not refactoring.
    """
    with cdb_dry_run(), AutoEnvVars(), raises(docker.errors.DockerException):
        put_artifact_image("tests/integration/test-pipefile.json")
