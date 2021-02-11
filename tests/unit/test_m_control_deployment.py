import pytest
from pytest import raises

from commands import run, CommandError
from tests.utils import *

DOMAIN = "app.compliancedb.com"
OWNER = "compliancedb"
NAME = "cdb-controls-test-pipeline"
IMAGE_NAME = "acme/road-runner:4.56"
SHA256 = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"


def test_raises_when_no_approvals(mocker):
    mocked_get = mocker.patch('commands.control_deployment_command.http_get_json', return_value=[])
    protocol = "docker://"
    ev = new_control_deployment_env()
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{IMAGE_NAME}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            with raises(CommandError):
                method, url, payload = run(env, fingerprinter, None)
    mocked_get.assert_called_once_with(
        "https://app.compliancedb.com/api/v1/projects/compliancedb/cdb-controls-test-pipeline/artifacts/efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212/approvals/",
        "MY_SUPER_SECRET_API_TOKEN"
    )


def new_control_deployment_env():
    ev = {
    }
    return {**core_env_vars("control_deployment"), **ev}