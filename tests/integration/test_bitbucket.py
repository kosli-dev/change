from cdb.bitbucket import put_bitbucket_pull_request

from tests.utils import ScopedEnvVars, CDB_DRY_RUN, verify_approval
import pytest

mocked_bitbucket_pull_requests_api_response = {
    "values": {
        "links": {
            "self": {"href": "test_self_uri", "name": "test_self"},
            "html": {"href": "test_html_uri", "name": "test_html"},
            "commits": {"href": "test_commit_uri", "name": "test_commits"},
            "approve": {"href": "test_approve_uri", "name": "test_approve"},
            "diff": {"href": "test_diff_uri", "name": "test_diff"},
            "diffstat": {"href": "test_diffstat_uri", "name": "test_diffstat"},
            "comments": {"href": "test_comments_uri", "name": "test_comments"},
            "activity": {"href": "test_activity_uri", "name": "test_activity"},
            "merge": {"href": "test_merge_uri", "name": "test_merge"},
            "decline": {"href": "test_decline_uri", "name": "test_decline"}
        },
        "id": "1",
        "title": "test pull request"
    }
}

@pytest.mark.skip
def test_only_required_env_vars(capsys, mocker):
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
        mocker.patch('requests.get',
                     return_value=MockedAPIResponse(200, mocked_bitbucket_pull_requests_api_response))
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

def test_exception_for_incomplete_bitbucket_api_resposne(capsys, mocker):
    # Test exception message(1) for get_pull_requests_from_bitbucket_api()
    # "Repository pull requests are still being indexed, please retry."
    with pytest.raises(SystemExit) as excinfo:
        mocker.patch("requests.get", return_value=MockedAPIResponse(202))
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
    assert excinfo.value.code == 1


def test_exception_for_non_existent_bitbucket_repository(capsys, mocker):
    # Test exception message(2) for get_pull_requests_from_bitbucket_api()
    # "Repository does not exists or pull requests are not indexed."
    # "Please make sure Pull Request Commit Links app is installed"
    with pytest.raises(SystemExit) as excinfo:
        mocker.patch("requests.get", return_value=MockedAPIResponse(404))
        put_bitbucket_pull_request("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])
    assert excinfo.value.code == 2


def test_exception_for_failed_pull_requests_fetching(capsys, mocker):
    # Test exception message(3) for get_pull_requests_from_bitbucket_api()
    # "Exception occurred in fetching pull requests. Http return code is 401"
    with pytest.raises(SystemExit) as excinfo:
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
