from cdb.create_deployment import create_deployment

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


# This is setting the CDB_ARTIFACT_SHA env-var
def test_CDB_ARTIFACT_SHA_is_defined(capsys):
    env = {
        "CDB_ARTIFACT_SHA": '1234567890',
    }
    with cdb_dry_run(), AutoEnvVars(env):
        create_deployment("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])
