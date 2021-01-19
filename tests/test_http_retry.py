from cdb.http import http_post_payload, http_put_payload, http_get_json
import cdb.http_retry as http_retry

from pytest import raises
from tests.utils import verify_approval, stub_http_503, retry_backoff_factor
import responses

MAX_RETRY_COUNT = 5


def test_total_retry_sleep_time_is_about_30_seconds():
    assert http_retry.HttpRetry().total_sleep_time() == 31  # 1+2+4+8+16


@responses.activate
def test_503_post_retries_5_times_then_raises_RetryError(capsys):
    url, payload, api_token = stub_http_503('POST', 1+MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(http_retry.Error) as exc_info:
        http_post_payload(url, payload, api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1+MAX_RETRY_COUNT
    verify_approval(capsys)


@responses.activate
def test_503_put_retries_5_times_then_raises_RetryError(capsys):
    url, payload, api_token = stub_http_503('PUT', 1+MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(http_retry.Error) as exc_info:
        http_put_payload(url, payload, api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1+MAX_RETRY_COUNT
    verify_approval(capsys)


@responses.activate
def test_503_get_retries_5_times_then_raises_RetryError(capsys):
    url, _, api_token = stub_http_503('GET', 1+MAX_RETRY_COUNT)

    with retry_backoff_factor(0.001), raises(http_retry.Error) as exc_info:
        http_get_json(url, api_token)

    assert exc_info.value.url() == url
    assert len(responses.calls) == 1+MAX_RETRY_COUNT
    verify_approval(capsys)


@responses.activate
def test_post_stops_retrying_when_non_503_and_returns_None(capsys):
    url, payload, api_token = stub_http_503('POST', 1+1)

    with retry_backoff_factor(0.001):
        response = http_post_payload(url, payload, api_token)

    assert response is None
    assert len(responses.calls) == 1+1+1
    verify_approval(capsys)


@responses.activate
def test_put_stops_retrying_when_non_503_and_returns_None(capsys):
    url, payload, api_token = stub_http_503('PUT', 1+1)

    with retry_backoff_factor(0.001):
        response = http_put_payload(url, payload, api_token)

    assert response is None
    assert len(responses.calls) == 1+1+1
    verify_approval(capsys)


@responses.activate
def test_get_stops_retrying_when_non_503_and_returns_response_json(capsys):
    url, _, api_token = stub_http_503('GET', 1+1)

    with retry_backoff_factor(0.001):
        response_json = http_get_json(url, api_token)

    assert response_json == {"success": 42}
    assert len(responses.calls) == 1+1+1
    verify_approval(capsys)
