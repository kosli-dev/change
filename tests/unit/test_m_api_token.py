from commands import External, run, DeclarePipeline
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_raises_when_api_token_not_set(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_API_TOKEN")

    with dry_run(ev) as env,raises(ChangeError):
        run(External(env=env))


def test_raises_when_api_token_is_empty_string(capsys):
    ev = core_env_vars()
    ev["MERKELY_API_TOKEN"] = ""

    with dry_run(ev) as env, raises(ChangeError):
        run(External(env=env))


def test_required_is_true():
    env = core_env_vars()
    command = DeclarePipeline(External(env=env))
    assert command.api_token.is_required('bitbucket')
