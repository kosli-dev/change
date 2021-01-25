from cdb.create_deployment import create_deployment

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_all_env_vars_uses_CDB_ARTIFACT_SHA(capsys):
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_SHA": '1234567890',
        "CDB_ENVIRONMENT": "production",
    }
    set_env_vars = {}
    with AutoEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        create_deployment("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])
