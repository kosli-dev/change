from lib.http import *
from lib.http_retry import HttpRetry, HttpRetryExhausted, MAX_RETRY_COUNT

from pytest import raises
import responses
from tests.utils import *


def test_total_retry_sleep_time_is_about_30_seconds():
    assert HttpRetry().total_sleep_time() == 31  # 1+2+4+8+16


@responses.activate
def test_no_retries_when_http_call_is_not_503(capsys):
    url, payload, api_token = stub_http_503('POST', 0)

    with retry_backoff_factor(0.001):
        http_post_payload(url=url, payload=payload, api_token=api_token)

    assert len(responses.calls) == 1


@responses.activate
def test_503_post_retries_5_times_then_raises_HttpRetryExhausted(capsys):
    url, payload, api_token = stub_http_503('POST', 1 + MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(HttpRetryExhausted) as exc_info:
        http_post_payload(url=url, payload=payload, api_token=api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1 + MAX_RETRY_COUNT
    assert_5_retries(capsys)


@responses.activate
def test_503_put_retries_5_times_then_raises_HttpRetryExhausted(capsys):
    url, payload, api_token = stub_http_503('PUT', 1 + MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(HttpRetryExhausted) as exc_info:
        http_put_payload(url=url, payload=payload, api_token=api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1 + MAX_RETRY_COUNT
    assert_5_retries(capsys)


@responses.activate
def test_503_get_retries_5_times_then_raises_HttpRetryExhausted(capsys):
    url, _, api_token = stub_http_503('GET', 1 + MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(HttpRetryExhausted) as exc_info:
        http_get_json(url=url, api_token=api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1 + MAX_RETRY_COUNT
    assert_5_retries(capsys)


@responses.activate
def test_post_stops_retrying_when_non_503_and_returns_None(capsys):
    url, payload, api_token = stub_http_503('POST', 1 + 1)

    with retry_backoff_factor(0.001):
        response = http_post_payload(url=url, payload=payload, api_token=api_token)

    assert response is None
    assert len(responses.calls) == 1 + 1 + 1
    assert_1_retry(capsys)


@responses.activate
def test_put_stops_retrying_when_non_503_and_returns_None(capsys):
    url, payload, api_token = stub_http_503('PUT', 1 + 1)

    with retry_backoff_factor(0.001):
        response = http_put_payload(url=url, payload=payload, api_token=api_token)

    assert response is None
    assert len(responses.calls) == 1 + 1 + 1
    assert_1_retry(capsys)


@responses.activate
def test_get_stops_retrying_when_non_503_and_returns_response_json(capsys):
    url, _, api_token = stub_http_503('GET', 1 + 1)

    with retry_backoff_factor(0.001):
        response_json = http_get_json(url=url, api_token=api_token)

    assert response_json == {'success': 42}
    assert len(responses.calls) == 1 + 1 + 1
    assert_1_retry(capsys)


def assert_5_retries(capsys):
    stdout = capsys_read(capsys).splitlines()
    assert stdout == [
        'Response.status=503, retrying in 0.001 seconds...',
        'Retry 1/5: response.status=503, retrying in 0.002 seconds...',
        'Retry 2/5: response.status=503, retrying in 0.004 seconds...',
        'Retry 3/5: response.status=503, retrying in 0.008 seconds...',
        'Retry 4/5: response.status=503, retrying in 0.016 seconds...',
        'Retry 5/5: response.status=503'
    ]


def assert_1_retry(capsys):
    stdout = capsys_read(capsys).splitlines()
    assert stdout == [
        'Response.status=503, retrying in 0.001 seconds...',
        'Retry 1/5: response.status=503, retrying in 0.002 seconds...',
        'Retry 2/5: response.status=200',
        '{"success": 42}'
    ]
