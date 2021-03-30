from .scoped_env_vars import ScopedEnvVars

DRY_RUN = {"MERKELY_DRY_RUN": "TRUE"}


def dry_run(ev, expected_set_vars=None):
    if expected_set_vars is None:
        expected_set_vars = {}
    return ScopedEnvVars({**DRY_RUN, **ev}, expected_set_vars)
