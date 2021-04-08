from lib.http import *
from lib.http_retry import HttpRetry, HttpRetryExhausted, MAX_RETRY_COUNT
from lib.stdout import Stdout

from pytest import raises
import responses
from tests.utils import *


def test_total_retry_sleep_time_is_about_30_seconds():
    assert HttpRetry(Stdout()).total_sleep_time() == 31  # 1+2+4+8+16


@responses.activate
def test_no_retries_when_http_call_is_not_503():
    url, payload, api_token = stub_http_503('POST', 0)

    with retry_backoff_factor(0.001):
        Http(Stdout()).post_payload(url, payload, api_token)

    assert len(responses.calls) == 1


@responses.activate
def test_503_post_retries_5_times_then_raises_HttpRetryExhausted():
    url, payload, api_token = stub_http_503('POST', 1 + MAX_RETRY_COUNT)

    stdout = Stdout()
    with retry_backoff_factor(0.001), raises(HttpRetryExhausted) as exc_info:
        Http(stdout).post_payload(url, payload, api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1 + MAX_RETRY_COUNT
    assert_5_retries(stdout.getvalue())


@responses.activate
def test_503_put_retries_5_times_then_raises_HttpRetryExhausted():
    url, payload, api_token = stub_http_503('PUT', 1 + MAX_RETRY_COUNT)

    stdout = Stdout()
    with retry_backoff_factor(0.001), raises(HttpRetryExhausted) as exc_info:
        Http(stdout).put_payload(url, payload, api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1 + MAX_RETRY_COUNT
    assert_5_retries(stdout.getvalue())


@responses.activate
def test_503_get_retries_5_times_then_raises_HttpRetryExhausted():
    url, _, api_token = stub_http_503('GET', 1 + MAX_RETRY_COUNT)

    stdout = Stdout()
    with retry_backoff_factor(0.001), raises(HttpRetryExhausted) as exc_info:
        Http(stdout).get_json(url, api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1 + MAX_RETRY_COUNT
    assert_5_retries(stdout.getvalue())


@responses.activate
def test_post_stops_retrying_when_non_503_and_returns_response():
    url, payload, api_token = stub_http_503('POST', 1 + 1)

    stdout = Stdout()
    with retry_backoff_factor(0.001):
        response = Http(stdout).post_payload(url, payload, api_token)

    assert response is not None
    assert len(responses.calls) == 1 + 1 + 1
    assert_1_retry(stdout.getvalue())


@responses.activate
def test_put_stops_retrying_when_non_503_and_returns_response():
    url, payload, api_token = stub_http_503('PUT', 1 + 1)

    stdout = Stdout()
    with retry_backoff_factor(0.001):
        response = Http(stdout).put_payload(url, payload, api_token)

    assert response is not None
    assert len(responses.calls) == 1 + 1 + 1
    assert_1_retry(stdout.getvalue())


@responses.activate
def test_get_stops_retrying_when_non_503_and_returns_response():
    url, _, api_token = stub_http_503('GET', 1 + 1)

    stdout = Stdout()
    with retry_backoff_factor(0.001):
        response = Http(stdout).get_json(url, api_token)

    assert response.json() == {'success': 42}
    assert len(responses.calls) == 1 + 1 + 1
    assert_1_retry(stdout.getvalue())


def assert_5_retries(stdout):
    lines = stdout.splitlines()
    assert lines == [
        'Response.status=503, retrying in 0.001 seconds...',
        'Retry 1/5: response.status=503, retrying in 0.002 seconds...',
        'Retry 2/5: response.status=503, retrying in 0.004 seconds...',
        'Retry 3/5: response.status=503, retrying in 0.008 seconds...',
        'Retry 4/5: response.status=503, retrying in 0.016 seconds...',
        'Retry 5/5: response.status=503'
    ]


def assert_1_retry(stdout):
    lines = stdout.splitlines()
    assert lines == [
        'Response.status=503, retrying in 0.001 seconds...',
        'Retry 1/5: response.status=503, retrying in 0.002 seconds...',
        'Retry 2/5: response.status=200',
    ]
