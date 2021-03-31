from commands import External, run
from errors import ChangeError

from pytest import raises
from tests.utils import *

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"

IMAGE_NAME = "acme/road-runner:4.56"
SHA256 = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"


def test_when_no_approvals_then_raises(mocker):
    mocked_get = mocker.patch('commands.runner.http_get_json', return_value=[])

    env = control_deployment_env()
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        with raises(ChangeError):
            run(external)

    mocked_get.assert_called_once_with(
        url=f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}/approvals/",
        api_token="MY_SUPER_SECRET_API_TOKEN",
        dry_run=False
    )


def test_when_approved_then_does_not_raise(mocker):
    mock_payload = [{"some_random": "stuff"}]
    mocked_get = mocker.patch('commands.runner.http_get_json', return_value=mock_payload)
    mocker.patch('commands.control_deployment.control_deployment_approved', return_value=True)

    env = control_deployment_env()
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    assert mock_payload == payload

    mocked_get.assert_called_once_with(
        url=f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}/approvals/",
        api_token="MY_SUPER_SECRET_API_TOKEN",
        dry_run=False
    )


def control_deployment_env():
    protocol = "docker://"
    ev = {"MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}"}
    return {**core_env_vars("control_deployment"), **ev}