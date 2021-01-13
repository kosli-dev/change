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
    hostname = 'https://app.compliancedb.com'
    route = "/api/v1/projects/compliancedb/cdb-controls-test-pipeline/approvals/"
    httpretty.register_uri(
        httpretty.POST,
        hostname + route,
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
        # The retry sleep delays are [ 0, 2, 4, 8, 16 ]
        # So this test will take ~30 seconds to pass :-(
        create_approval("integration_tests/test-pipefile.json", env=env)
    except requests.exceptions.RetryError:
        captured = capsys.readouterr()
        stdout = captured.out
        assert "POST failed" in stdout
        assert "URL={}".format(route) in stdout
        assert "STATUS=503" in stdout
        assert "Retrying in 2 seconds (1/4)" in stdout
        assert "Retrying in 4 seconds (2/4)" in stdout
        assert "Retrying in 8 seconds (3/4)" in stdout
        assert "Retrying in 16 seconds (4/4)" in stdout
        assert len(httpretty.latest_requests()) == 5+1


