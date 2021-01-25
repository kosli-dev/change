from cdb.put_pipeline import put_pipeline

from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars(capsys):
    env = {
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }
    set_env_vars = {}
    with AutoEnvVars(CDB_DRY_RUN, set_env_vars):
        put_pipeline("tests/integration/test-pipefile.json", env)
    verify_approval(capsys)


def test_all_env_vars(capsys):
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }
    set_env_vars = {}
    with AutoEnvVars(CDB_DRY_RUN, set_env_vars):
        put_pipeline("tests/integration/test-pipefile.json", env)
    verify_approval(capsys)
