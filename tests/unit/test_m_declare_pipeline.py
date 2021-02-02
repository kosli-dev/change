from commands import command_processor, Context
from tests.utils import *


def test_green(capsys):
    with dry_run(core_env_vars()) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code == 0
    verify_approval(capsys)
