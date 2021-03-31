from lib.in_dry_run import *
from lib.http import *

from tests.utils import *


def test_dry_run_can_be_set_locally():
    assert not in_dry_run({"MERKELY_DRY_RUN": ""})
    assert not in_dry_run({"MERKELY_DRY_RUN": "FALSE"})
    assert in_dry_run({"MERKELY_DRY_RUN": "TRUE"})


def test_run_can_be_set_globally():
    assert not in_dry_run({"MERKELY_API_TOKEN": ""})
    assert not in_dry_run({"MERKELY_API_TOKEN": "FALSE"})
    assert in_dry_run({"MERKELY_API_TOKEN": "DRY_RUN"})


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
