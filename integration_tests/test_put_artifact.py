from cdb.put_artifact import put_artifact
from os import environ
from approvaltests.approvals import verify
from approvaltests.reporters import PythonNativeReporter
from tests.cdb_dry_run import cdb_dry_run
from tests.set_env_vars import SetEnvVars


def test_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    with cdb_dry_run():
        put_artifact("integration_tests/test-pipefile.json")

    captured = capsys.readouterr()
    verify(captured.out, PythonNativeReporter())


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_missing(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests_data/put-artifact.txt",
        "CDB_ARTIFACT_SHA": "UNDEFINED"
    }
    with cdb_dry_run(), SetEnvVars(env):
        put_artifact("integration_tests/test-pipefile.json")

    captured = capsys.readouterr()
    verify(captured.out, PythonNativeReporter())
