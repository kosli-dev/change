from commands import command_processor
from tests.utils import *


def test_host_not_set_defaults(capsys):
    ev = core_env_vars()
    ev.pop("MERKELY_HOST")

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code == 0
    verify_approval(capsys)


def test_host_set(capsys):
    ev = core_env_vars()
    ev["MERKELY_HOST"] = "https://test.merkely.com"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code == 0
    verify_approval(capsys)
