from os import environ


class AutoEnvVars(object):
    def __init__(self, env_vars):
        self._env_vars = env_vars
        for (name, value) in env_vars.items():
            environ[name] = value

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        for name in self._env_vars:
            environ.pop(name)

