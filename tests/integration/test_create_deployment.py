from cdb.create_deployment import create_deployment

from tests.utils import ScopedEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    # sha provided explicitly
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": '99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212',
        "CDB_ENVIRONMENT": "production",
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_deployment("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # mock Docker which calculates the sha
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/runner:4.56",
        "CDB_ENVIRONMENT": "production",
    }
    sha = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        create_deployment("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    # Mock openssl which calculates the sha
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_ENVIRONMENT": "production",
    }
    sha = "cccdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        create_deployment("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys, mocker):
    # required and optional env-vars
    env = {
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
        "CDB_ENVIRONMENT": "production",
        "CDB_DESCRIPTION": "branch coverage",  # optional
        "CDB_CI_BUILD_URL": "https://gitlab/build/1996",  # optional
        "CDB_USER_DATA": "/some/file.json"  # optional
    }
    sha = "cccdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        mocker.patch('cdb.create_deployment.load_user_data', return_value={"x": 42})
        create_deployment("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
