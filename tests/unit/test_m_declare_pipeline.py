from commands import run, DeclarePipeline
from tests.utils import *


def test_green(capsys):
    with dry_run(core_env_vars()) as env, scoped_merkelypipe_json():
        run(env=env)

    verify_approval(capsys)


def test_summary_is_not_empty():
    context = {}
    command = DeclarePipeline(context)
    assert len(command.summary) > 0
