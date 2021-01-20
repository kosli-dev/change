from tests.unit.utils import AutoEnvVars


def cdb_dry_run():
    """
    Important tests use this to prevent env-vars
    set in one test from affecting subsequent tests.
    """
    return AutoEnvVars({"CDB_DRY_RUN": "TRUE"})
