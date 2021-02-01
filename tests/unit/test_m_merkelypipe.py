
from commands import command_processor, Context
from tests.utils import verify_approval, ScopedEnvVars, ScopedFileCopier, CDB_DRY_RUN, make_context


def test_file_not_found(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }
    # no /Merkelypipe.json
    with ScopedEnvVars({**CDB_DRY_RUN, **ev}) as env:
        status_code = command_processor.execute(make_context(env))

    assert status_code != 0
    verify_approval(capsys)


"""
Possible negative test cases:

File not valid json
json has no key "owner"
json "owner" value not string
Pipe is a directory not a file (volume mount issue)
"""
