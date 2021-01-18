import os
from approvaltests.approvals import verify
from approvaltests.reporters import PythonNativeReporter
from tests.cdb_dry_run import cdb_dry_run
from cdb.put_artifact import put_artifact

def test_put_artifact_message_when_env_var_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    env = {
        "CDB_HOST": "http://app2.compliancedb.com",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commits/3451345234523453245",
		"CDB_ARTIFACT_GIT_COMMIT": "134125123541234123513425",
		"CDB_CI_BUILD_URL": "https://gitlab/build/1234",
		"CDB_BUILD_NUMBER": "1234",
		"xx_CDB_ARTIFACT_FILENAME": "integration_tests/test-pipefile.json"
    }
    for name, value in env.items():
        os.environ[name] = value
    
    with cdb_dry_run():
        put_artifact("integration_tests/test-pipefile.json")

    captured = capsys.readouterr()
    verify(captured.out + captured.err, PythonNativeReporter())

