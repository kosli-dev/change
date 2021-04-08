from commands import External, main
from tests.utils import *

IMAGE_NAME = "acme/widget:4.67"
SHA256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"


def test_GET_command(mocker):
    mocked_get = mocker.patch('lib.http_retry.http.get', return_value=HttpStatus(200))
    env = control_deployment_env()
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        exit_code = main(external)

    assert exit_code == 144
    # assert mocked.assert_called_once_with(...)
    mocked_get.assert_called_once()


def test_PUT_command(mocker):
    mocked_put = mocker.patch('lib.http_retry.http.put', return_value=HttpStatus(200))
    env = log_evidence_env()
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        exit_code = main(external)

    assert exit_code == 0
    # assert mocked.assert_called_once_with(...)
    mocked_put.assert_called_once()


def test_POST_command(mocker):
    mocked_post = mocker.patch('lib.http_retry.http.post', return_value=HttpStatus(200))
    env = log_deployment_env()
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        exit_code = main(external)

    assert exit_code == 0
    # assert mocked.assert_called_once_with(...)
    mocked_post.assert_called_once()


def test_command_raises_when_http_response_is_not_200_or_201(mocker):
    mocked_post = mocker.patch('lib.http_retry.http.post', return_value=HttpStatus(403))
    env = log_deployment_env()
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        exit_code = main(external)

    assert exit_code != 0
    # assert mocked.assert_called_once_with(...)
    mocked_post.assert_called_once()


class HttpStatus:
    def __init__(self, code):
        self._code = code

    @property
    def status_code(self):
        return self._code

    @property
    def text(self):
        return ""

    def json(self):
        return {}


DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
CI_BUILD_URL = "https://gitlab/build/1956"
DESCRIPTION = "some description"
ENVIRONMENT = "production"
USER_DATA = "/app/tests/data/user_data.json"

PROTOCOL = "docker://"


def control_deployment_env():
    ev = {"MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}"}
    return {**core_env_vars("control_deployment"), **ev}


def log_evidence_env():
    ev = {
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        "MERKELY_CI_BUILD_URL": CI_BUILD_URL,
        "MERKELY_IS_COMPLIANT": "TRUE",
        "MERKELY_EVIDENCE_TYPE": "unit_test",
        "MERKELY_DESCRIPTION": "branch coverage"
    }
    return {**core_env_vars("log_evidence"), **ev}


def log_deployment_env():
    ev = {
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        "MERKELY_CI_BUILD_URL": CI_BUILD_URL,
        "MERKELY_ENVIRONMENT": ENVIRONMENT,
        "MERKELY_DESCRIPTION": DESCRIPTION,
        "MERKELY_USER_DATA": USER_DATA,
    }
    return {**core_env_vars("log_deployment"), **ev}
