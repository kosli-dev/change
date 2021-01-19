from cdb.put_artifact import put_artifact

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


def test_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    with cdb_dry_run():
        put_artifact("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_UNDEFINED(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests_data/coverage.txt",
        "CDB_ARTIFACT_SHA": "UNDEFINED"
    }
    with cdb_dry_run(), AutoEnvVars(env):
        put_artifact("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])


# This is setting the CDB_ARTIFACT_SHA env-var
def test_message_when_env_var_CDB_ARTIFACT_SHA_is_not_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests_data/coverage.txt",
    }
    with cdb_dry_run(), AutoEnvVars(env):
        put_artifact("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])
