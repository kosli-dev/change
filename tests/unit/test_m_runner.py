from commands import run
from tests.utils import *


def test_fails_when_merkely_command_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_COMMAND")

    with dry_run(ev) as env:
        assert run(env) != 0

    verify_approval(capsys)


def test_fails_when_merkely_command_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_COMMAND"] = ""

    with dry_run(ev) as env:
        assert run(env) != 0

    verify_approval(capsys)


def test_fails_when_merkely_command_is_unknown(capsys):
    ev = core_env_vars()
    ev["MERKELY_COMMAND"] = "wibble"

    with dry_run(ev) as env:
        assert run(env) != 0

    verify_approval(capsys)
