from cdb.put_artifact_image import put_artifact_image
import docker

from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_all_env_vars_defined(capsys):
    # artifact sha comes from CDB_ARTIFACT_SHA
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:3.4",
        "CDB_ARTIFACT_SHA": "a7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/12037940e4e7503055d8a8eea87e177f04f14616",
        "CDB_ARTIFACT_GIT_COMMIT": "12037940e4e7503055d8a8eea87e177f04f14616",
        "CDB_CI_BUILD_URL": "https://gitlab/build/5641"
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_no_env_vars_raises_DockerException():
    """
    This is not the desired behaviour, but until more tests are
    in place we are not refactoring.
    """
    set_env_vars = {}
    with AutoEnvVars(CDB_DRY_RUN, set_env_vars), raises(docker.errors.DockerException):
        put_artifact_image("tests/integration/test-pipefile.json")


