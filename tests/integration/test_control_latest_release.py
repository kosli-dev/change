from cdb.control_latest_release import control_latest_release

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars_uses_CDB_ARTIFACT_SHA(capsys, mocker):
    # sha provided explicitly

    mocked_project_file = "tests/integration/test-pipefile.json"
    mocked_json = {
        "approvals": [],
        "base_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "description": "Test release for the release project",
        "release_number": 1234,
        "src_commit_list": [
            "e412ad6f7ea530ee9b83df964a0dde2b477be728",
            "e412ad6f7ea530ee9b83df964a0dde2b477be729"
        ],
        "state": "UNAPPROVED",
        "target_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    }
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": '99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212',
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.control_latest_release.parse_cmd_line', return_value=mocked_project_file)
        mocker.patch('cdb.control_latest_release.http_get_json', return_value=mocked_json)
        control_latest_release()
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    # artifact sha calculated from CDB_ARTIFACT_DOCKER_IMAGE

    mocked_project_file = "tests/integration/test-pipefile.json"
    mocked_json = {
        "approvals": [],
        "base_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "description": "Test release for the release project",
        "release_number": 1234,
        "src_commit_list": [
            "e412ad6f7ea530ee9b83df964a0dde2b477be728",
            "e412ad6f7ea530ee9b83df964a0dde2b477be729"
        ],
        "state": "UNAPPROVED",
        "target_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    }

    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/widget:3.4",
    }
    sha = "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.control_latest_release.parse_cmd_line', return_value=mocked_project_file)
        mocker.patch('cdb.control_latest_release.http_get_json', return_value=mocked_json)
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        control_latest_release()
    verify_approval(capsys, ["out"])


def test_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    # artifact sha calculated from CDB_ARTIFACT_FILENAME

    mocked_project_file = "tests/integration/test-pipefile.json"
    mocked_json = {
        "approvals": [],
        "base_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "description": "Test release for the release project",
        "release_number": 1234,
        "src_commit_list": [
            "e412ad6f7ea530ee9b83df964a0dde2b477be728",
            "e412ad6f7ea530ee9b83df964a0dde2b477be729"
        ],
        "state": "UNAPPROVED",
        "target_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    }

    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "some/artifact/file.txt",
    }
    sha = "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.control_latest_release.parse_cmd_line', return_value=mocked_project_file)
        mocker.patch('cdb.control_latest_release.http_get_json', return_value=mocked_json)
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        control_latest_release()
    verify_approval(capsys, ["out"])


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys, mocker):
    # sha provided explicitly

    mocked_project_file = "tests/integration/test-pipefile.json"
    mocked_json = {
        "approvals": [],
        "base_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "description": "Test release for the release project",
        "release_number": 1234,
        "src_commit_list": [
            "e412ad6f7ea530ee9b83df964a0dde2b477be728",
            "e412ad6f7ea530ee9b83df964a0dde2b477be729"
        ],
        "state": "UNAPPROVED",
        "target_artifact": "99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    }
    env = {
        "CDB_HOST": "http://test.compliancedb.com",  # optional
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": '99cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212',
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.control_latest_release.parse_cmd_line', return_value=mocked_project_file)
        mocker.patch('cdb.control_latest_release.http_get_json', return_value=mocked_json)
        control_latest_release()
    verify_approval(capsys, ["out"])
