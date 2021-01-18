from cdb.put_pipeline import put_pipeline

from tests.cdb_dry_run import cdb_dry_run
from tests.verify_approval import verify_approval


def test_put_pipeline(capsys):
    env = {
        "CDB_HOST": "http://app2.compliancedb.com",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }

    with cdb_dry_run():
        put_pipeline("integration_tests/test-pipefile.json", env)

    verify_approval(capsys)
