import os
from approvaltests.approvals import verify

from cdb.create_approval import create_approval
from tests.test_git import TEST_REPO_ROOT


def test_put_approval(capsys):
    os.environ["CDB_DRY_RUN"] = "TRUE"
    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,
    }
    create_approval("integration_tests/test-pipeline.json", env=env)
    captured = capsys.readouterr()
    verify(captured.out + captured.err)
