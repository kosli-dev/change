from commands import External, run
from errors import ChangeError

from pytest import raises
from tests.utils import *

DOMAIN = "app.compliancedb.com"
OWNER = "compliancedb"
NAME = "cdb-controls-test-pipeline"
IMAGE_NAME = "acme/road-runner:4.56"
SHA256 = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
MERKELY_PIPE = "Merkelypipe.compliancedb.json"


def test_when_no_approvals_then_raises(mocker):
    mocked_get = mocker.patch('commands.control_deployment.http_get_json', return_value=[])

    ev = new_control_deployment_env()

    with dry_run(ev) as env, scoped_merkelypipe_json(filename=MERKELY_PIPE):
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            with raises(ChangeError):
                run(external)

    mocked_get.assert_called_once_with(
        "https://app.compliancedb.com/api/v1/projects/compliancedb/cdb-controls-test-pipeline/artifacts/efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212/approvals/",
        "MY_SUPER_SECRET_API_TOKEN"
    )


def test_when_approved_then_does_not_raise(mocker):
    mock_payload = [{"some_random": "stuff"}]
    mocked_get = mocker.patch('commands.control_deployment.http_get_json', return_value=mock_payload)
    mocker.patch('commands.control_deployment.control_deployment_approved', return_value=True)

    ev = new_control_deployment_env()

    with dry_run(ev) as env, scoped_merkelypipe_json(filename=MERKELY_PIPE):
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)
            assert mock_payload == payload

    mocked_get.assert_called_once_with(
        "https://app.compliancedb.com/api/v1/projects/compliancedb/cdb-controls-test-pipeline/artifacts/efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212/approvals/",
        "MY_SUPER_SECRET_API_TOKEN"
    )


def new_control_deployment_env():
    protocol = "docker://"
    ev = {"MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}"}
    return {**core_env_vars("control_deployment"), **ev}