from commands import command_processor, Context
from tests.utils import *


def test_raises_when_host_not_set(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        # "MERKELY_HOST": "https://test.merkely.com"
    }

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_raises_when_host_is_empty_string(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": ""
    }

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)
