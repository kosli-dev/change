import os
from approvaltests.approvals import verify

from cdb.put_pipeline import put_pipeline


def test_put_pipeline(capsys):
    os.environ["CDB_DRY_RUN"] = "TRUE"
    env = {
        "CDB_HOST": "http://app2.compliancedb.com",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }
    put_pipeline("integration_tests/test-pipeline.json", env=env)
    captured = capsys.readouterr()
    verify(captured.out + captured.err)