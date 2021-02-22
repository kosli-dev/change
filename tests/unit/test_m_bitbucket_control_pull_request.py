from cdb.bitbucket import put_bitbucket_pull_request
from commands import run

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_control_pull_request"

DOMAIN = "app.compliancedb.com"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

BB = 'bitbucket.org'
ORG = 'acme'
REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"

DESCRIPTION = "branch coverage"
EVIDENCE_TYPE = "unit_test"


def test_bitbucket(capsys, mocker):
    env = {
        "CDB_HOST": f"https://{DOMAIN}",
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_SHA": SHA256,

        "BITBUCKET_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "BITBUCKET_API_USER": "test_user",

        "BITBUCKET_WORKSPACE": ORG,
        "BITBUCKET_REPO_SLUG": REPO,
        "BITBUCKET_COMMIT": COMMIT,
    }

    with dry_run(env):
        mocker.patch('cdb.bitbucket.requests.get',
                     return_value=MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response))
        mocker.patch('cdb.bitbucket.json.loads', return_value=mocked_bitbucket_pull_requests_api_response)
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
            "description": "Bitbucket pull request",
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
        "evidence_type": "pull_request"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    #...




class MockedAPIResponse:
    def __init__(self, status_code, response_body=None):
        self.status_code = status_code
        self.response_body = response_body

    @property
    def text(self):
        return str(self.response_body)


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
        "MERKELY_IS_COMPLIANT": "TRUE",
        "MERKELY_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "MERKELY_DESCRIPTION": DESCRIPTION,

        "BITBUCKET_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "BITBUCKET_API_USER": "test_user",

        "BITBUCKET_WORKSPACE": ORG,
        "BITBUCKET_REPO_SLUG": REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
