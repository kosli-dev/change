from commands import command_processor, Context
from tests.utils import *


def test_raises_when_host_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_HOST")

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_raises_when_host_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_HOST"] = ""

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def core_env_vars():
    return {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }
