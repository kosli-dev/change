from os import environ


def cdb_dry_run():
    """
    Important tests use this to prevent env-vars
    set in one test from polluting subsequent tests.
    """
    return SetEnv("CDB_DRY_RUN", "TRUE")


class SetEnv(object):
    def __init__(self, key, value):
        self._key = key
        environ[key] = value

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        environ.pop(self._key)
