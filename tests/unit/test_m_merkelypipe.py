from commands import run
from tests.utils import *


def test_file_not_found(capsys):
    with dry_run(core_env_vars()) as env:
        # no /Merkelypipe.json
        status_code = run(env)

    assert status_code != 0
    verify_approval(capsys)


def test_invalid_json(capsys):
    with dry_run(core_env_vars()) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", "/Merkelypipe.json"):
            status_code = run(env)

    assert status_code != 0
    verify_approval(capsys)


def test_is_a_dir(capsys):
    with dry_run(core_env_vars()) as env:
        with ScopedDirCopier("/test_src", "/Merkelypipe.json"):
            status_code = run(env)

    assert status_code != 0
    verify_approval(capsys)


"""
Possible negative test cases:

json has no key "owner"
json "owner" value not string
"""
