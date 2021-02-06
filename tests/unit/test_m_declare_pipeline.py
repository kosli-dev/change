from commands import run
from tests.utils import *


def test_green(capsys):
    with dry_run(core_env_vars()) as env, scoped_merkelypipe_json():
        run(env)

    verify_approval(capsys)
