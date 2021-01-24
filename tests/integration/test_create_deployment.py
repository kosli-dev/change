from cdb.create_deployment import create_deployment

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


# This is setting the CDB_ARTIFACT_SHA env-var
def test_CDB_ARTIFACT_SHA_is_defined(capsys):
    env = {
        "CDB_ARTIFACT_SHA": '1234567890',
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_deployment("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])
