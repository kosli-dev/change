from cdb.put_artifact import put_artifact

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


def test_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    with cdb_dry_run(), AutoEnvVars({}):
        put_artifact("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_UNDEFINED(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
        "CDB_ARTIFACT_SHA": "UNDEFINED"
    }
    with cdb_dry_run(), AutoEnvVars(env):
        put_artifact("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_not_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
    }

    set_env_vars = {
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    }

    with cdb_dry_run(), AutoEnvVars(env, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])
