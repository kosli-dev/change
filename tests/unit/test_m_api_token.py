from commands import run
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_raises_when_api_token_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_API_TOKEN")

    with dry_run(ev) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json"):
            with raises(ChangeError):
                run(env=env)


def test_raises_when_api_token_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_API_TOKEN"] = ""

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with raises(ChangeError):
            run(env=env)
