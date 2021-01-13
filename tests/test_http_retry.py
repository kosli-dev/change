import httpretty
import pytest
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
        "XXXX_api_token": "not-None"
    }

    with backoff_factor(0.001), pytest.raises(requests.exceptions.RetryError):
        create_approval("integration_tests/test-pipefile.json", env=env)

    expected_lines = (
        "POST failed",
        "URL={}".format(route),  # request.url drops the protocol and hostname :(
        "STATUS=503",
        "Retrying in 0.002 seconds (1/4)...failed",
        "Retrying in 0.004 seconds (2/4)...failed",
        "Retrying in 0.008 seconds (3/4)...failed",
        "Retrying in 0.016 seconds (4/4)...failed"
    )
    stderr = capsys.readouterr().err
    for line in expected_lines:
        assert line in stderr, line

    assert len(httpretty.latest_requests()) == 5+1


def backoff_factor(f):
    return WithBackOffFactor(f)


class WithBackOffFactor(object):
    def __init__(self, factor):
        self._factor = factor

    def __enter__(self):
        self._original = cdb.http_retry.RETRY_BACKOFF_FACTOR
        cdb.http_retry.RETRY_BACKOFF_FACTOR = self._factor

    def __exit__(self, _type, _value, _traceback):
        cdb.http_retry.RETRY_BACKOFF_FACTOR = self._original

