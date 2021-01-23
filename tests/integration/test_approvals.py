from cdb.create_approval import create_approval

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval
from tests.unit.test_git import TEST_REPO_ROOT


# This is setting the CDB_ARTIFACT_SHA env-var
def test_put_approval(capsys):
    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,
    }

    with AutoEnvVars(CDB_DRY_RUN):
        create_approval("tests/integration/test-pipefile.json", env)

    verify_approval(capsys, ["out", "err"])
