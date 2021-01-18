from cdb.http import http_post_payload, http_put_payload, http_get_json
import cdb.http_retry as http_retry
from requests.exceptions import RetryError

import json
from pytest import raises
from tests.utils import verify_approval
import responses

MAX_RETRY_COUNT = http_retry.MAX_RETRY_COUNT


def test_total_retry_sleep_time_is_about_30_seconds():
    assert http_retry.total_sleep_time() == 31  # 1+2+4+8+16


@responses.activate
def test_503_post_retries_5_times_then_raises_RetryError(capsys):
    url, payload, api_token = stub_http_503('POST', 1+MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(RetryError):
        http_post_payload(url, payload, api_token)

    verify_approval(capsys)
    assert len(responses.calls) == 1+MAX_RETRY_COUNT


@responses.activate
def test_503_put_retries_5_times_then_raises_RetryError(capsys):
    url, payload, api_token = stub_http_503('PUT', 1+MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(RetryError):
        http_put_payload(url, payload, api_token)

    verify_approval(capsys)
    assert len(responses.calls) == 1+MAX_RETRY_COUNT


@responses.activate
def test_503_get_retries_5_times_then_raises_RetryError(capsys):
    url, _, api_token = stub_http_503('GET', 1+MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(RetryError):
        http_get_json(url, api_token)

    verify_approval(capsys)
    assert len(responses.calls) == 1+MAX_RETRY_COUNT


def stub_http_503(method, count):
    # Eg during deployment rollover
    url = "https://test.compliancedb.com/api/v1/{}/".format(method.lower())

    def request_callback(request):
        headers = {}
        if len(responses.calls) < count:
            return 503, headers, json.dumps({"error": "service unavailable"})
        else:
            return 200, headers, json.dumps({})

    responses.add_callback(
        getattr(responses, method),
        url=url,
        callback=request_callback
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
        self._original = http_retry.RETRY_BACKOFF_FACTOR
        http_retry.RETRY_BACKOFF_FACTOR = self._factor

    def __exit__(self, _type, _value, _traceback):
        http_retry.RETRY_BACKOFF_FACTOR = self._original
