
"""
This command is used to declare a pipeline in Merkely.  It is invoked:

docker run \
        --env MERKELY_COMMAND=declare_pipeline \
        \
        --env MERKELY_API_TOKEN=${YOUR_API_TOKEN} \
        --env MERKELY_HOST=https://app.merkely.com \
        --rm \
        --volume ${PWD}/${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change
"""

from commands import command_processor, Context
from tests.utils import *


def test_green(capsys):
    ev = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": "https://test.merkely.com"
    }

    with dry_run(ev) as env, scoped_merkelypipe_json():
        status_code = command_processor.execute(make_context(env))

    assert status_code == 0
    verify_approval(capsys)
