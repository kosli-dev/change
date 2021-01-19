import os


class AutoEnvVars(object):
    def __init__(self, env_vars={}):
        self._env_vars = env_vars

    def __enter__(self):
        for (name, value) in self._env_vars.items():
            os.environ[name] = value
        return self

    def __exit__(self, _type, _value, _traceback):
        for name in self._env_vars:
            os.environ.pop(name)

