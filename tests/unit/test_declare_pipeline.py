
"""
This command is used to declare a pipeline in Merkely.  It is invoked:

docker run \
        --env MERKELY_COMMAND=declare_pipeline \
        \
        --env MERKELY_API_TOKEN=${YOUR_API_TOKEN} \
        --rm \
        --volume ${PWD}/${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change


Possible negative test cases:

File not found
File not valid json
File has key "owner"
File "owner" value not string
Pipe is a directory not a file (volume mount issue)
api token env variable not set
api token empty
"""


# command processor test

import command_processor
from tests.utils import verify_approval, AutoEnvVars, CDB_DRY_RUN
from tests.utils.auto_file_copier import AutoFileCopier

"""
class Command:
    pass

class DeclarePipelineCommand(Command):
    
    def execute():
        pass
    
    def validate_arguments(env):
        pass

"""


def test_command_processor_declare_pipeline_green(capsys):
    env = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
    }

    with AutoEnvVars(CDB_DRY_RUN), AutoFileCopier("/app/tests/data/Merkelypipe.json", "/Merkelypipe.json"):
        status_code = command_processor.execute(env)

    assert status_code == 0
    verify_approval(capsys)

