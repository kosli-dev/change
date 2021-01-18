from tests.set_env_vars import SetEnvVars


def cdb_dry_run():
    """
    Important tests use this to prevent env-vars
    set in one test from affecting subsequent tests.
    """
    return SetEnvVars({"CDB_DRY_RUN": "TRUE"})
