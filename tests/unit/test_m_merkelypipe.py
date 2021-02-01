from commands import command_processor, Context
from tests.utils import *


def test_file_not_found(capsys):
    with dry_run(declare_pipeline_env()) as env:
        # no /Merkelypipe.json
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_invalid_json(capsys):
    with dry_run(declare_pipeline_env()) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", "/Merkelypipe.json"):
            status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_is_a_dir(capsys):
    with dry_run(declare_pipeline_env()) as env:
        with ScopedDirCopier("/test_src", "/Merkelypipe.json"):
            status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def declare_pipeline_env():
    return {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }


"""
Possible negative test cases:

json has no key "owner"
json "owner" value not string
"""
