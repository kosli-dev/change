from commands import Context, command_runner
from tests.utils import *


def test_raises_when_merkely_command_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_COMMAND")

    with dry_run(ev) as env:
        status_code = command_runner.run(Context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_raises_when_merkely_command_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_COMMAND"] = ""

    with dry_run(ev) as env:
        status_code = command_runner.run(Context(env))

    assert status_code != 0
    verify_approval(capsys)
