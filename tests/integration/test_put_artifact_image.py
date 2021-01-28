from cdb.put_artifact_image import put_artifact_image
import docker

from pytest import raises
from tests.utils import ScopedEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # artifact sha calculated from CDB_ARTIFACT_DOCKER_IMAGE
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:3.4",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/12037940e4e7503055d8a8eea87e177f04f14616",
        "CDB_ARTIFACT_GIT_COMMIT": "12037940e4e7503055d8a8eea87e177f04f14616",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        sha = "ddcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ee"
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys, mocker):
    # artifact sha comes direct from CDB_ARTIFACT_SHA
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/12037940e4e7503055d8a8eea87e177f04f14616",
        "CDB_ARTIFACT_GIT_COMMIT": "92037940e4e7503055d8a8eea87e177f04f14616",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_all_env_vars(capsys):
    # artifact sha comes direct from CDB_ARTIFACT_SHA
    env = {
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_API_TOKEN": "6599831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "b7cdaef69c676c2466571d9933380d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/12037940e4e7503055d8a8eea87e177f04f14616",
        "CDB_ARTIFACT_GIT_COMMIT": "82037940e4e7503055d8a8eea87e177f04f14616",
        "CDB_CI_BUILD_URL": "https://gitlab/build/351",  # optional
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact_image("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_no_env_vars_raises_DockerException():
    """
    This is not the desired behaviour, but until more tests are
    in place we are not refactoring.
    """
    set_env_vars = {}

    with ScopedEnvVars(CDB_DRY_RUN, set_env_vars), raises(docker.errors.DockerException):
        put_artifact_image("tests/integration/test-pipefile.json")


