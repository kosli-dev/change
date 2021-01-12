import httpretty
import requests

from cdb.create_approval import create_approval
from tests.test_git import TEST_REPO_ROOT


"""
At first this tried to use the responses library to stub the http calls.
https://github.com/getsentry/responses
Alas it does not (currently) work when you are http-retrying.
See https://github.com/getsentry/responses/issues/135
"""


@httpretty.activate
def test_503_POST_retries_5_times(capsys):
    # This is mostly for deployment rollover
    url = 'https://app.compliancedb.com/api/v1/projects/compliancedb/cdb-controls-test-pipeline/approvals/'
    httpretty.register_uri(
        httpretty.POST,
        url,
        responses=[
            httpretty.Response(
                body='{"error": "service unavailable"}',
                status=503,
            )
        ]
    )
    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,
    }
    try:
        # The 5 retry sleep delays are [ 0.5, 1, 2, 4, 8 ]
        # So this test will take 15.5 seconds to pass :-(
        create_approval("integration_tests/test-pipefile.json", env=env)
    except requests.exceptions.RetryError:
        assert len(httpretty.latest_requests()) == 5+1


