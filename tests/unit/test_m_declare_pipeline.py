from commands import command_processor, Context
from tests.utils import *


def test_green(capsys):
    with dry_run(core_env_vars()) as env, scoped_merkelypipe_json():
        command_processor.execute(Context(env))

    verify_approval(capsys)
