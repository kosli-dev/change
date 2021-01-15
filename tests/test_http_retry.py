import requests
from cdb.http import http_post_payload, http_put_payload, http_get_json
import cdb.http_retry

import httpretty
import pytest
from approvaltests.approvals import verify
from approvaltests.reporters import PythonNativeReporter


"""
We are using httpretty to stub the http calls.
This works when you are using a requests.packages.urllib3.util.retry.Retry 
object inside a requests.adapters.HTTPAdapter object mounted inside a
requests.Session object.
Packages we tried that did not work in this situation are:
1) responses (https://github.com/getsentry/responses)
   See https://github.com/getsentry/responses/issues/135
2) requests_mock (https://requests-mock.readthedocs.io/en/latest/)
"""


def test_total_retry_sleep_time_is_about_30_seconds():
    assert cdb.http_retry.LoggingRetry.total_sleep_time() == 31  # 1+2+4+8+16


@httpretty.activate
def test_503_post_retries_5_times(capsys):
    scheme_host = 'https://test.compliancedb.com'
    path = "/api/v1/projects/compliancedb/cdb-controls-test-pipeline/approvals/"
    url = scheme_host + path
    http_stub_503('POST', url, service_unavailable_payload())

    with retry_backoff_factor(0.001), pytest.raises(requests.exceptions.RetryError):
        payload = {"name": "cern", "template": ["artefact", "unit_test"]}
        http_post_payload(url, payload, "the-api-token")

    captured = capsys.readouterr()
    verify(captured.out + captured.err, PythonNativeReporter())
    assert len(httpretty.latest_requests()) == 5+1


@httpretty.activate
def test_503_put_retries_5_times(capsys):
    scheme_host = 'https://test.compliancedb.com'
    path = "/api/v1/any/path/"
    url = scheme_host + path
    http_stub_503('PUT', url, service_unavailable_payload())

    with retry_backoff_factor(0.001), pytest.raises(requests.exceptions.RetryError):
        payload = {"name": "git", "template": ["artefact", "coverage"]}
        http_put_payload(url, payload, "the-api-token")

    captured = capsys.readouterr()
    verify(captured.out + captured.err, PythonNativeReporter())
    assert len(httpretty.latest_requests()) == 5+1


@httpretty.activate
def test_503_get_retries_5_times(capsys):
    scheme_host = 'https://test.compliancedb.com'
    path = "/api/v1/any/path/"
    url = scheme_host + path
    http_stub_503('GET', url, service_unavailable_payload())

    with retry_backoff_factor(0.001), pytest.raises(requests.exceptions.RetryError):
        http_get_json(url, "the-api-token")

    captured = capsys.readouterr()
    verify(captured.out + captured.err, PythonNativeReporter())
    assert len(httpretty.latest_requests()) == 5+1


def http_stub_503(method, url, payload):
    httpretty.register_uri(
        getattr(httpretty, method),
        url,
        responses=[
            httpretty.Response(
                body=payload,
                status=503,  # Eg during deployment rollover
            )
        ]
    )


def service_unavailable_payload():
    return '{"error": "service unavailable"}'


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

