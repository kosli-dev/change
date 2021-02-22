from pipe import BitbucketPipe, schema

from tests.utils import *


def test_required_env_vars(capsys):
    env = {
        "CDB_COMMAND": "put_pipeline",
        "CDB_PIPELINE_DEFINITION": "tests/data/pipefile.json",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        pipe.run()
    verify_approval(capsys)


