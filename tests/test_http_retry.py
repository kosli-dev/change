import httpretty
import pytest
import requests

from cdb.create_approval import create_approval
from tests.test_git import TEST_REPO_ROOT
import cdb.http_retry


"""
We are using httpretty to stub the http calls.
This works when you are using a requests.packages.urllib3.util.retry.Retry 
object inside a requests.adapters.HTTPAdapter object mounted inside a
requests.Session object.
Packages we have tried that did not work are:
1) responses (https://github.com/getsentry/responses)
   See https://github.com/getsentry/responses/issues/135
2) requests_mock (https://requests-mock.readthedocs.io/en/latest/)
"""


def test_total_retry_time_is_about_30_seconds():
    assert cdb.http_retry.LoggingRetry().total_backoff_time() == 31  # 1+2+4+8+16


@httpretty.activate
def test_503_post_retries_5_times(capsys):
    hostname = 'https://test.compliancedb.com'
    route = "/api/v1/projects/compliancedb/cdb-controls-test-pipeline/approvals/"

    httpretty.register_uri(
        httpretty.POST,
        hostname + route,
        responses=[
            httpretty.Response(
                body='{"error": "service unavailable"}',
                status=503,  # Eg deployment rollover
            )
        ]
    )

    env = {
        "CDB_HOST": hostname,
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,
        "CDB_API_TOKEN": "not-None"  # To prevent DeprecationWarning:  Non-string usernames
    }

    with retry_backoff_factor(0.001), pytest.raises(requests.exceptions.RetryError):
        create_approval("integration_tests/test-pipefile.json", env)

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


def retry_backoff_factor(f):
    return RetryBackOffFactor(f)


class RetryBackOffFactor(object):
    def __init__(self, factor):
        self._factor = factor

    def __enter__(self):
        self._original = cdb.http_retry.RETRY_BACKOFF_FACTOR
        cdb.http_retry.RETRY_BACKOFF_FACTOR = self._factor

    def __exit__(self, _type, _value, _traceback):
        cdb.http_retry.RETRY_BACKOFF_FACTOR = self._original

