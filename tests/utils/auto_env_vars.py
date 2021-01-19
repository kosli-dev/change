import copy
import os


class AutoEnvVars(object):
    def __init__(self, env_vars={}):
        self._true_env_vars = copy.deepcopy(os.environ)
        self._auto_env_vars = env_vars

    def __enter__(self):
        for (name, value) in self._auto_env_vars.items():
            os.environ[name] = value
        return self

    def __exit__(self, _type, _value, _traceback):
        os.environ.clear()
        for (name, value) in self._true_env_vars.items():
            os.environ[name] = value

