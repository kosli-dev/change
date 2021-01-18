from cdb.put_artifact import put_artifact

from tests.verify_approval import verify_approval
from tests.cdb_dry_run import cdb_dry_run
from tests.auto_env_vars import AutoEnvVars


def test_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    with cdb_dry_run():
        put_artifact("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_missing(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests_data/put-artifact.txt",
        "CDB_ARTIFACT_SHA": "UNDEFINED"
    }
    with cdb_dry_run(), AutoEnvVars(env):
        put_artifact("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])
