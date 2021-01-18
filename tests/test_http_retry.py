import requests
from cdb.http import http_post_payload, http_put_payload, http_get_json
import cdb.http_retry

import httpretty
import json
from pytest import raises
from tests.utils import verify_approval


"""
We are using httpretty to stub the http calls.
https://pypi.org/project/httpretty/
This works when you are using a requests.packages.urllib3.util.retry.Retry 
object inside a requests.adapters.HTTPAdapter object mounted inside a
requests.Session object.
Packages we tried that did not work in this situation are:
1) responses 
   See https://github.com/getsentry/responses
   See https://github.com/getsentry/responses/issues/135
2) requests_mock 
   See https://requests-mock.readthedocs.io/en/latest/
"""


def test_total_retry_sleep_time_is_30_seconds():
    assert cdb.http_retry.total_sleep_time() == 30  # 0+2+4+8+16


@httpretty.activate
def test_503_post_retries_5_times(capsys):
    url, payload, api_token = stub_http('POST', 503)

    with retry_backoff_factor(0.001), raises(requests.exceptions.RetryError):
        http_post_payload(url, payload, api_token)

    verify_approval(capsys)
    assert len(httpretty.latest_requests()) == 1+5


@httpretty.activate
def test_503_put_retries_5_times(capsys):
    url, payload, api_token = stub_http('PUT', 503)

    with retry_backoff_factor(0.001), raises(requests.exceptions.RetryError):
        http_put_payload(url, payload, api_token)

    verify_approval(capsys)
    assert len(httpretty.latest_requests()) == 1+5


@httpretty.activate
def test_503_get_retries_5_times(capsys):
    url, _, api_token = stub_http('GET', 503)

    with retry_backoff_factor(0.001), raises(requests.exceptions.RetryError):
        http_get_json(url, api_token)

    verify_approval(capsys)
    assert len(httpretty.latest_requests()) == 1+5


def stub_http(method, status):
    url = "https://test.compliancedb.com/api/v1/{}/".format(method.lower())
    httpretty.register_uri(
        getattr(httpretty, method),
        url,
        responses=[
            httpretty.Response(
                body=json.dumps({"error": "service unavailable"}),
                status=503  # Eg during deployment rollover
            )
        ]
    )
    if method == "GET":
        payload = None
    if method == "POST":
        payload = {"name": "cern", "template": ["artefact", "unit_test"]}
    if method == "PUT":
        payload = {"name": "git", "template": ["artefact", "coverage"]}
    api_token = ""
    return url, payload, api_token


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

