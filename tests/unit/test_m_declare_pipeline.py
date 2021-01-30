
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


import command_processor
from tests.utils import verify_approval, ScopedEnvVars, ScopedFileCopier, CDB_DRY_RUN


def test_command_processor_declare_pipeline_green(capsys):
    env = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}) as ev:
        with ScopedFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json"):
            status_code = command_processor.execute(ev)

    assert status_code == 0
    verify_approval(capsys)


"""
Possible negative test cases:
File not found
File not valid json
File has key "owner"
File "owner" value not string
Pipe is a directory not a file (volume mount issue)
api token env variable not set
api token empty
"""

"""
class Command:
    pass

class DeclarePipelineCommand(Command):

    def execute():
        pass

    def validate_arguments(env):
        pass
"""
