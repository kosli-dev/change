from cdb.put_artifact import put_artifact

from os import environ
from approvaltests.approvals import verify
from approvaltests.reporters import PythonNativeReporter
from tests.cdb_dry_run import cdb_dry_run


def test_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    with cdb_dry_run():
        put_artifact("integration_tests/test-pipefile.json")

    captured = capsys.readouterr()
    verify(captured.out, PythonNativeReporter())


def test_message_when_env_var_CDB_ARTIFACT_SHA_is_missing(capsys):
    with cdb_dry_run():
        with SetEnv({"CDB_ARTIFACT_FILENAME": "tests_data/put-artifact.txt"}):
            with SetEnv({"CDB_ARTIFACT_SHA": "UNDEFINED"}):
                put_artifact("integration_tests/test-pipefile.json")

    captured = capsys.readouterr()
    verify(captured.out, PythonNativeReporter())


class SetEnv(object):
    def __init__(self, env_vars):
        self._env_vars = env_vars
        for (name, value) in env_vars.items():
            environ[name] = value

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        for name in self._env_vars:
            environ.pop(name)


