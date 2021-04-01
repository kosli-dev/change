from commands import Command, External
from lib.http import *
from tests.utils import *

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_setting_dry_run_locally_using_MERKELY_DRY_RUN_env_var_is_TRUE():
    assert not in_dry_run(dry_run="FALSE")
    assert in_dry_run(dry_run="TRUE")


def test_setting_dry_run_globally_using_MERKELY_API_TOKEN_env_var_is_DRY_RUN():
    assert not in_dry_run(api_token=API_TOKEN)
    assert in_dry_run(api_token="DRY_RUN")


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


def in_dry_run(*, api_token=None, dry_run=None):
    if api_token is None:
        api_token = API_TOKEN
    if dry_run is None:
        dry_run = "FALSE"
    env = {
        'MERKELY_COMMAND': 'log_artifact',
        'MERKELY_API_TOKEN': api_token,
        'MERKELY_DRY_RUN': dry_run
    }
    command = Command(External(env=env))
    return command.in_dry_run
