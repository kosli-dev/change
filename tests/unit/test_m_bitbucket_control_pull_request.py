from cdb.bitbucket import put_bitbucket_pull_request
from commands import run

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_control_pull_request"

DOMAIN = "app.compliancedb.com"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

BITBUCKET_API_TOKEN = "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BITBUCKET_API_USER = "test_user"

BB = 'bitbucket.org'
ORG = 'acme'
REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"

DESCRIPTION = "Bitbucket pull request"
EVIDENCE_TYPE = "pull_request"


def test_bitbucket(capsys, mocker):
    env = {
        "CDB_HOST": f"https://{DOMAIN}",
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_SHA": SHA256,

        "BITBUCKET_API_TOKEN": BITBUCKET_API_TOKEN,
        "BITBUCKET_API_USER": BITBUCKET_API_USER,

        "BITBUCKET_WORKSPACE": ORG,
        "BITBUCKET_REPO_SLUG": REPO,
        "BITBUCKET_COMMIT": COMMIT,
    }

    with dry_run(env):
        rv = MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response)
        mocker.patch('cdb.bitbucket.requests.get', return_value=rv)
        mocker.patch('cdb.cdb_utils.load_project_configuration', return_value=test_pipefile)
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
        mocker.stopall()

    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{ORG}/{REPO}/artifacts/{SHA256}"
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
            "url": f"https://{BB}/{ORG}/{REPO}"
        },
        "evidence_type": EVIDENCE_TYPE
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_control_pull_request_env()
    merkelypipe = "Merkelypipe.acme-roadrunner.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            rv1 = MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response)
            mocker.patch('commands.control_pull_request.requests.get', return_value=rv1)
            method, url, payload = run(env=env, docker_fingerprinter=fingerprinter)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


class MockedAPIResponse:
    def __init__(self, status_code, response_body):
        self.status_code = status_code
        self.response_body = response_body

    @property
    def text(self):
        import json
        return json.dumps(self.response_body)


mocked_bitbucket_pull_requests_api_response = {
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
    "owner": ORG,
    "name": REPO,
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
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "MERKELY_DESCRIPTION": DESCRIPTION,

        "BITBUCKET_API_TOKEN": BITBUCKET_API_TOKEN,
        "BITBUCKET_API_USER": BITBUCKET_API_USER,

        "BITBUCKET_WORKSPACE": ORG,
        "BITBUCKET_REPO_SLUG": REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
