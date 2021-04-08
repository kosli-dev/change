from commands import External, run, DeclarePipeline
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_raises_when_api_token_not_set():
    env = dry_run(core_env_vars('log_artifact'))
    env.pop("MERKELY_API_TOKEN")

    with raises(ChangeError):
        run(External(env=env))


def test_raises_when_api_token_is_empty_string():
    env = dry_run(core_env_vars('log_artifact'))
    env["MERKELY_API_TOKEN"] = ""

    with raises(ChangeError):
        run(External(env=env))


def test_required_is_true():
    env = dry_run(core_env_vars('log_artifact'))
    command = DeclarePipeline(External(env=env))
    assert command.api_token.is_required('bitbucket')
