from cdb.put_pipeline import put_pipeline

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


def test_put_pipeline(capsys):
    env = {
        "CDB_HOST": "http://app2.compliancedb.com",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }

    with cdb_dry_run(), AutoEnvVars({}):
        put_pipeline("tests/integration/test-pipefile.json", env)

    verify_approval(capsys)
