from cdb.put_artifact import put_artifact

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


def test_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    with cdb_dry_run(), AutoEnvVars():
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


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_not_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests_data/coverage.txt",
    }

    with cdb_dry_run(), AutoEnvVars(env) as ev_context:
        put_artifact("integration_tests/test-pipefile.json")

    expected_new_env_vars = {
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc",
        "CDB_ARTIFACT_FILENAME": "tests_data/coverage.txt"
    }
    actual_new_env_vars = ev_context.new_env_vars()
    assert expected_new_env_vars == actual_new_env_vars

    verify_approval(capsys, ["out"])
