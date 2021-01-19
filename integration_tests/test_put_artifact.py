from cdb.put_artifact import put_artifact
import os

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
        # This is setting the CDB_ARTIFACT_SHA env-var!
        put_artifact("integration_tests/test-pipefile.json")

    created_env_vars = ["CDB_ARTIFACT_FILENAME", "CDB_ARTIFACT_SHA"]
    assert sorted(list(ev_context.new_env_vars().keys())) == sorted(created_env_vars)
    assert ev_context.is_creating_env_var("CDB_ARTIFACT_SHA")
    assert ev_context.is_creating_env_var("CDB_ARTIFACT_FILENAME")
    verify_approval(capsys, ["out"])
