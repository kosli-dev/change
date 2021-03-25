from commands import run, main, External

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_control_pull_request"

BITBUCKET_API_TOKEN = "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BITBUCKET_API_USER = "test_user"

BB = 'bitbucket.org'
BB_ORG = 'acme'
BB_REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

DOMAIN = "app.compliancedb.com"
OWNER = "acme"
PIPELINE = "road-runner"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"

DESCRIPTION = "Bitbucket pull request"
EVIDENCE_TYPE = "pull_request"


def test_bitbucket(capsys, mocker):
    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
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
            "url": f"https://{BB}/{BB_ORG}/{BB_REPO}"
        },
        "evidence_type": EVIDENCE_TYPE
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_control_pull_request_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            rv1 = MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response())
            mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    capsys_read(capsys)

    # Change of behaviour
    expected_payload['contents']['url'] = f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}"

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def test_bitbucket_not_compliant_raises(capsys, mocker):
    # make merkely call
    ev = new_control_pull_request_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            response = mocked_bitbucket_pull_requests_api_response()
            response['values'] = []
            rv1 = MockedAPIResponse(200, response)
            mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)
            external = External(env=env, docker_fingerprinter=fingerprinter)
            exit_code = main(external)

    assert exit_code != 0

    stdout = capsys_read(capsys)
    lines = stdout.split("\n")
    last_line = lines[-2]  # ignore trailing newline
    assert last_line[:6] == 'Error:'


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


test_pipefile = {
    "owner": OWNER,
    "name": PIPELINE,
    "description": "Test Pipeline Controls for Merkely",
    "visibility": "public",
    "template": [
        "artifact",
        "unit_test",
        "coverage"
    ]
}


def new_control_pull_request_env():
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
