
"""
This command is used to declare a pipeline in Merkely.  It is invoked:

docker run \
        --env MERKELY_COMMAND=declare_pipeline \
        \
        --rm \
        --env MERKELY_API_TOKEN=${YOUR_API_TOKEN} \
        --volume ${PWD}/${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change
"""

from commands import command_processor, Context
from tests.utils import verify_approval, ScopedEnvVars, ScopedFileCopier, CDB_DRY_RUN


def test_green(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **ev}) as env:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json"):
            status_code = command_processor.execute(make_context(env))

    assert status_code == 0
    verify_approval(capsys)


def make_context(env):
    context = type('context', (), {})()
    context.env = env
    return context


"""
Possible negative test cases:
File not found
File not valid json
json has no key "owner"
json "owner" value not string
Pipe is a directory not a file (volume mount issue)
api token env variable not set
api token empty
"""
