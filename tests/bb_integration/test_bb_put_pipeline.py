from pipe import BitbucketPipe, schema

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars(capsys):
    env = {
        "CDB_COMMAND": "put_pipeline",
        "CDB_PIPELINE_DEFINITION": "tests/data/pipefile.json",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        pipe.run()
    verify_approval(capsys)


