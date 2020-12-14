from cdb.create_deployment import create_deployment_payload


def test_create_deployment_payload():
    env = {"CDB_ARTIFACT_SHA": "1234", "CDB_ENVIRONMENT": "test-env", "CDB_DESCRIPTION": "Description"}
    payload = create_deployment_payload(env)

    assert payload == {
        "artifact_sha256": "1234",
        'build_url': None,
        "environment": "test-env",
        "description": "Description",
    }


def test_create_deployment_payload_with_build_url():
    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_ENVIRONMENT": "test-env",
        "CDB_DESCRIPTION": "Description",
        "CDB_CI_BUILD_URL": "https://myciserver.org/hadroncollider/11"
    }
    payload = create_deployment_payload(env)

    assert payload == {
        "artifact_sha256": "1234",
        'build_url': env["CDB_CI_BUILD_URL"],
        "environment": "test-env",
        "description": "Description"
    }


def test_create_deployment_payload_with_user_data(mocker):
    mock_json = mocker.patch('cdb.create_deployment.load_user_data')
    mock_json.return_value = {"super_cool": "user data"}

    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_ENVIRONMENT": "test-env",
        "CDB_DESCRIPTION": "Description",
        "CDB_USER_DATA": "/some/file/user_data.json"
    }
    payload = create_deployment_payload(env)

    assert payload == {
        "artifact_sha256": "1234",
        'build_url': None,
        "environment": "test-env",
        "description": "Description",
        "user_data": {"super_cool": "user data"}
    }
