from commands import run, main, External
from errors import ChangeError

from tests.utils import *
from pytest import raises

BB = 'bitbucket.org'
BB_ORG = 'acme'
BB_REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "road-runner"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"

DESCRIPTION = "Bitbucket pull request"
EVIDENCE_TYPE = "pull_request"

BITBUCKET_API_TOKEN = "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BITBUCKET_API_USER = "test_user"


def test_bitbucket(capsys, mocker):
    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": DESCRIPTION,
            "is_compliant": True,
            "source": [
                {
                    "approvers": "test_username",
                    "pullRequestMergeCommit": COMMIT,
                    "pullRequestState": "OPEN",
                    "pullRequestURL": "test_html_uri"
                }
            ],
            "url": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}"
        },
        "evidence_type": EVIDENCE_TYPE
    }

    rv1 = MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response())
    mocked_get = mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)

    ev = control_pull_request_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    silence(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    expected_mock_calls = [
        mocker.call(f'https://api.bitbucket.org/2.0/repositories/{OWNER}/{PIPELINE}/commit/{COMMIT}/pullrequests',
                    auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN)),
        mocker.call('test_self_uri', auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN))]
    assert mocked_get.call_args_list == expected_mock_calls


def test_bitbucket_pull_requests_with_no_approvers(capsys, mocker):
    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": DESCRIPTION,
            "is_compliant": True,
            "source": [
                {
                    "pullRequestMergeCommit": COMMIT,
                    "pullRequestState": "OPEN",
                    "pullRequestURL": "test_html_uri"
                }
            ],
            "url": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}"
        },
        "evidence_type": EVIDENCE_TYPE
    }

    response = mocked_bitbucket_pull_requests_api_response()
    response['participants'] = []
    rv1 = MockedAPIResponse(200, response)
    mocked_get = mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)

    ev = control_pull_request_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    stdout = capsys_read(capsys).split("\n")
    assert stdout[3] == "No approvers found"
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    expected_mock_calls = [
        mocker.call(f'https://api.bitbucket.org/2.0/repositories/{OWNER}/{PIPELINE}/commit/{COMMIT}/pullrequests',
                    auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN)),
        mocker.call('test_self_uri', auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN))]
    assert mocked_get.call_args_list == expected_mock_calls


def X_test_bitbucket_not_compliant_raises(capsys, mocker):
    # Turned off to get dry-run from api_token in place
    response = mocked_bitbucket_pull_requests_api_response()
    response['values'] = []
    rv1 = MockedAPIResponse(200, response)
    mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)

    ev = control_pull_request_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            exit_code = main(external)

    assert exit_code != 0

    stdout = capsys_read(capsys)
    lines = stdout.split("\n")
    last_line = lines[-2]  # ignore trailing newline
    assert last_line[:6] == 'Error:'


def test_bitbucket_api_response_202(capsys, mocker):
    rv1 = MockedAPIResponse(202, {})
    mocked_get = mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)

    ev = control_pull_request_env()
    with dry_run(ev) as env:
        with raises(ChangeError) as exc:
            external = External(env=env)
            _, _, _ = run(external)

    silence(capsys)
    assert str(exc.value) == "Repository pull requests are still being indexed, please retry."

    expected_mock_calls = [
        mocker.call(f'https://api.bitbucket.org/2.0/repositories/{OWNER}/{PIPELINE}/commit/{COMMIT}/pullrequests',
                    auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN))]
    assert mocked_get.call_args_list == expected_mock_calls


def test_bitbucket_api_response_404(capsys, mocker):
    rv1 = MockedAPIResponse(404, {})
    mocked_get = mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)

    ev = control_pull_request_env()
    with dry_run(ev) as env:
        with raises(ChangeError) as exc:
            external = External(env=env)
            _, _, _ = run(external)

    silence(capsys)
    expected_error_message = " ".join([
        "Repository does not exists or pull requests are not indexed.",
        "Please make sure Pull Request Commit Links app is installed"
    ])
    assert str(exc.value) == expected_error_message

    expected_mock_calls = [
        mocker.call(f'https://api.bitbucket.org/2.0/repositories/{OWNER}/{PIPELINE}/commit/{COMMIT}/pullrequests',
                    auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN))]
    assert mocked_get.call_args_list == expected_mock_calls


def test_bitbucket_api_response_505(capsys, mocker):
    # Test error message in case of unexpected status code from Bitbucket API
    rv1 = MockedAPIResponse(505, {"Message": "Test error"})
    mocked_get = mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)

    ev = control_pull_request_env()
    with dry_run(ev) as env:
        with raises(ChangeError) as exc:
            external = External(env=env)
            _, _, _ = run(external)

    silence(capsys)
    message = 'Exception occurred in fetching pull requests. Http return code is 505'
    message += '\n    {"Message": "Test error"}'
    assert str(exc.value) == message

    expected_mock_calls = [
        mocker.call(f'https://api.bitbucket.org/2.0/repositories/{OWNER}/{PIPELINE}/commit/{COMMIT}/pullrequests',
                    auth=(BITBUCKET_API_USER, BITBUCKET_API_TOKEN))]
    assert mocked_get.call_args_list == expected_mock_calls

class MockedAPIResponse:
    def __init__(self, status_code, response_body):
        self.status_code = status_code
        self.response_body = response_body

    @property
    def text(self):
        import json
        return json.dumps(self.response_body)


def mocked_bitbucket_pull_requests_api_response():
    return {
        "values": [{
            "links": {
                "self": {"href": "test_self_uri", "name": "test_self"},
                "html": {"href": "test_html_uri", "name": "test_html"},
            },
            "id": "1",
            "title": "test pull request",
        }],
        "state": "OPEN",
        "participants": [
            {
                "approved": True,
                "state": "approved",
                "user": {
                    "display_name": "test_username"
                }
            }
        ]
    }


def control_pull_request_env():
    return {
        "MERKELY_COMMAND": "control_pull_request",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",

        "MERKELY_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "MERKELY_DESCRIPTION": DESCRIPTION,

        "BITBUCKET_API_TOKEN": BITBUCKET_API_TOKEN,
        "BITBUCKET_API_USER": BITBUCKET_API_USER,

        "BITBUCKET_WORKSPACE": BB_ORG,
        "BITBUCKET_REPO_SLUG": BB_REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
