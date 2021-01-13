import httpretty
import requests

from cdb.create_approval import create_approval
from tests.test_git import TEST_REPO_ROOT
import cdb.http_retry

"""
At first this tried to use the responses library to stub the http calls.
https://github.com/getsentry/responses
Alas it does not (currently) work when you are http-retrying.
See https://github.com/getsentry/responses/issues/135
"""


def test_total_retry_time_is_about_30_seconds():
    assert cdb.http_retry.LoggingRetry().total_backoff_time() == 31  # 1+2+4+8+16


@httpretty.activate
def test_503_post_retries_5_times(capsys):
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
        original_backoff_factor = cdb.http_retry.RETRY_BACKOFF_FACTOR
        cdb.http_retry.RETRY_BACKOFF_FACTOR = 0.001  # otherwise test takes 30 seconds
        create_approval("integration_tests/test-pipefile.json", env=env)
    except requests.exceptions.RetryError:
        captured = capsys.readouterr()
        stdout = captured.out
        assert "POST failed" in stdout
        # request.url drops the protocol and hostname :(
        assert "URL={}".format(route) in stdout
        assert "STATUS=503" in stdout
        assert "Retrying in 0.002 seconds (1/4)" in stdout
        assert "Retrying in 0.004 seconds (2/4)" in stdout
        assert "Retrying in 0.008 seconds (3/4)" in stdout
        assert "Retrying in 0.016 seconds (4/4)" in stdout
        assert len(httpretty.latest_requests()) == 5+1
    finally:
        cdb.http_retry.RETRY_BACKOFF_FACTOR = original_backoff_factor
        assert cdb.http_retry.RETRY_BACKOFF_FACTOR != 0.001

