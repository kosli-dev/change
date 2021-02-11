from commands import run, CommandError
from tests.utils import *
from pytest import raises


def test_raises_when_not_found(capsys):
    with dry_run(core_env_vars()) as env, raises(CommandError):
        # no /Merkelypipe.json
        run(env)


def test_raises_when_invalid_json(capsys):
    with dry_run(core_env_vars()) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", "/Merkelypipe.json"):
            with raises(CommandError):
                run(env)


def test_raises_when_is_a_dir(capsys):
    with dry_run(core_env_vars()) as env:
        with ScopedDirCopier("/test_src", "/Merkelypipe.json"):
            with raises(CommandError):
                run(env)


"""
Possible further tests:

json has no key "owner"
json "owner" value not string
"""
