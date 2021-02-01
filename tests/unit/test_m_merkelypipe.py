
from commands import command_processor, Context
from tests.utils import *


def test_file_not_found(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }
    with ScopedEnvVars({**CDB_DRY_RUN, **ev}) as env:
        # no /Merkelypipe.json
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_invalid_json(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **ev}) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", "/Merkelypipe.json"):
            status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


def test_is_a_dir(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **ev}) as env:
        with ScopedDirCopier("/test_src", "/Merkelypipe.json"):
            status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)



"""
Possible negative test cases:

json has no key "owner"
json "owner" value not string
"""