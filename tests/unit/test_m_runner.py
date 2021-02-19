from commands import run
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_raises_when_merkely_command_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_COMMAND")

    with dry_run(ev) as env, raises(ChangeError):
            run(env=env)


def test_raises_when_merkely_command_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_COMMAND"] = ""

    with dry_run(ev) as env, raises(ChangeError):
        run(env=env)


def test_raises_when_merkely_command_is_unknown(capsys):
    ev = core_env_vars()
    ev["MERKELY_COMMAND"] = "wibble"

    with dry_run(ev) as env, raises(ChangeError):
        run(env=env)
