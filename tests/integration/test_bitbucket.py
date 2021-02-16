from cdb.bitbucket import put_bitbucket_pull_request
from tests.utils import *
from pytest import raises

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_bitbucket"

# This object is used to mock API response from Bitbucket API's GET/pullrequests endpoint
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

# This object is used to mock return value of cdb_utils.load_project_configuration()
test_pipefile = {
    "name": "cdb-controls-test-pipeline",
    "description": "Test Pipeline Controls for ComplianceDB",
    "owner": "compliancedb",
    "visibility": "public",
    "template": [
        "artifact",
        "unit_test",
        "coverage"
    ]
}


def test_only_required_env_vars(capsys, mocker):
    # Test for put_bitbucket_pull_request
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    env = {
        "CDB_API_TOKEN": "1239831f4ee3b79e7c5b7e0ebe75d67aa66e7aab",
        "BITBUCKET_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "BITBUCKET_WORKSPACE": "test_project",
        "BITBUCKET_REPO_SLUG": "test_repo",
        "BITBUCKET_COMMIT": "12037940e4e7503055d8a8eea87e177f04f14616",
        "BITBUCKET_API_USER": "test_user",
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}):
        mocker.patch('cdb.bitbucket.requests.get',
                     return_value=MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response))
        mocker.patch('cdb.bitbucket.json.loads', return_value=mocked_bitbucket_pull_requests_api_response)
        mocker.patch('cdb.cdb_utils.load_project_configuration', return_value=test_pipefile)
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
        mocker.stopall()
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_only_required_env_vars"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "Bitbucket pull request",
            "is_compliant": True,
            "source": [
                {
                    "approvers": "test_username",
                    "pullRequestMergeCommit": "12037940e4e7503055d8a8eea87e177f04f14616",
                    "pullRequestState": "OPEN",
                    "pullRequestURL": "test_html_uri"
                }
            ],
            "url": "https://bitbucket.org/test_project/test_repo"
        },
        "evidence_type": "pull_request"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_all_env_vars(capsys, mocker):
    # Test for put_bitbucket_pull_request
    sha256 = "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    env = {
        "CDB_API_TOKEN": "1239831f4ee3b79e7c5b7e0ebe75d67aa66e7aab",
        "BITBUCKET_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": sha256,
        "BITBUCKET_WORKSPACE": "test_project",
        "BITBUCKET_REPO_SLUG": "test_repo",
        "BITBUCKET_COMMIT": "12037940e4e7503055d8a8eea87e177f04f14616",
        "BITBUCKET_API_USER": "test_user",
        "CDB_FORCE_COMPLIANT": "TRUE",  # optional
        "CDB_FAIL_PIPELINE": "TRUE",  # optional
        "CDB_HOST": "https://app.compliancedb.com"  # optional
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}):
        mocker.patch('cdb.bitbucket.requests.get',
                     return_value=MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response))
        mocker.patch('cdb.bitbucket.json.loads', return_value=mocked_bitbucket_pull_requests_api_response)
        mocker.patch('cdb.cdb_utils.load_project_configuration', return_value=test_pipefile)
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
        mocker.stopall()
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "Bitbucket pull request",
            "is_compliant": True,
            "source": [
                {
                    "approvers": "test_username",
                    "pullRequestMergeCommit": "12037940e4e7503055d8a8eea87e177f04f14616",
                    "pullRequestState": "OPEN",
                    "pullRequestURL": "test_html_uri"
                }
            ],
            "url": "https://bitbucket.org/test_project/test_repo"
        },
        "evidence_type": "pull_request"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_put_bitbucket_pull_request_with_no_approvers_in_pr(capsys, mocker):
    # Test for put_bitbucket_pull_request when there are  0 approvers in Bitbucket GET/pullrequests response
    bitbucket_pr_response_without_participants = {
        "values": [{
            "links": {
                "self": {"href": "test_self_uri", "name": "test_self"},
                "html": {"href": "test_html_uri", "name": "test_html"},
            },
            "id": "1",
            "title": "test pull request",
        }],
        "state": "OPEN",
        "participants": []
    }
    env = {
        "CDB_API_TOKEN": "1239831f4ee3b79e7c5b7e0ebe75d67aa66e7aab",
        "BITBUCKET_API_TOKEN": "6199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": "b7cdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef",
        "BITBUCKET_WORKSPACE": "test_project",
        "BITBUCKET_REPO_SLUG": "test_repo",
        "BITBUCKET_COMMIT": "12037940e4e7503055d8a8eea87e177f04f14616",
        "BITBUCKET_API_USER": "test_user",
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}):
        mocker.patch('cdb.bitbucket.requests.get',
                     return_value=MockedAPIResponse(200, bitbucket_pr_response_without_participants))
        mocker.patch('cdb.bitbucket.json.loads', return_value=bitbucket_pr_response_without_participants)
        mocker.patch('cdb.cdb_utils.load_project_configuration', return_value=test_pipefile)
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
        mocker.stopall()
    verify_approval(capsys, ["out"])


def test_exception_for_incomplete_bitbucket_api_resposne(capsys, mocker):
    # Test for put_bitbucket_pull_request
    # Test exception message(1) for get_pull_requests_from_bitbucket_api()
    # "Repository pull requests are still being indexed, please retry."
    with raises(SystemExit) as excinfo:
        mocker.patch("requests.get", return_value=MockedAPIResponse(202))
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
    assert excinfo.value.code == 1


def test_exception_for_non_existent_bitbucket_repository(capsys, mocker):
    # Test for put_bitbucket_pull_request
    # Test exception message(2) for get_pull_requests_from_bitbucket_api()
    # "Repository does not exists or pull requests are not indexed."
    # "Please make sure Pull Request Commit Links app is installed"
    with raises(SystemExit) as excinfo:
        mocker.patch("requests.get", return_value=MockedAPIResponse(404))
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
    assert excinfo.value.code == 2


def test_exception_for_failed_pull_requests_fetching(capsys, mocker):
    # Test for put_bitbucket_pull_request
    # Test exception message(3) for get_pull_requests_from_bitbucket_api()
    # "Exception occurred in fetching pull requests. Http return code is 401"
    with raises(SystemExit) as excinfo:
        mocker.patch("requests.get", return_value=MockedAPIResponse(401))
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
    assert excinfo.value.code == 3


class MockedAPIResponse:
    def __init__(self, status_code, response_body=None):
        self.status_code = status_code
        self.response_body = response_body

    @property
    def text(self):
        return str(self.response_body)
