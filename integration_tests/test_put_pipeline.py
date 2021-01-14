import os
from approvaltests.approvals import verify
from tests.cdb_dry_run import cdb_dry_run
from cdb.put_pipeline import put_pipeline


def test_put_pipeline(capsys):
    env = {
        "CDB_HOST": "http://app2.compliancedb.com",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }
    with cdb_dry_run():
        put_pipeline("integration_tests/test-pipefile.json", env=env)
    captured = capsys.readouterr()
    verify(captured.out + captured.err)