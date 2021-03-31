from lib.http import *

from tests.utils import *


def test_put_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('lib.http.req')

    with silent(capsys), dry_run({}):
        http_put_payload(url="https://app.example.com", payload={}, api_token="")

    requests.put.assert_not_called()


def test_post_dry_run_doesnt_call(mocker, capsys):
    requests = mocker.patch('lib.http.req')

    with silent(capsys), dry_run({}):
        http_post_payload(url="https://www.example.com", payload={}, api_token="")

    requests.post.assert_not_called()
