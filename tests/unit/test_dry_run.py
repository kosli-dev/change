from lib.http import *

from tests.utils import *


def test_get_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('lib.http.req')

    with silent(capsys), dry_run({}):
        http_get_json(url="https://app.example.com", api_token="", dry_run=True)

    requests.get.assert_not_called()


def test_put_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('lib.http.req')

    with silent(capsys), dry_run({}):
        http_put_payload(url="https://app.example.com", payload={}, api_token="", dry_run=True)

    requests.put.assert_not_called()


def test_post_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('lib.http.req')

    with silent(capsys), dry_run({}):
        http_post_payload(url="https://www.example.com", payload={}, api_token="", dry_run=True)

    requests.post.assert_not_called()
