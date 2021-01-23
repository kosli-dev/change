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
        self._new_env_vars = self._newly_set_env_vars()
        os.environ.clear()
        for (name, value) in self._true_env_vars.items():
            os.environ[name] = value

    def _newly_set_env_vars(self):
        result = {}
        enter_keys = self._true_env_vars.keys()
        exit_keys = os.environ.keys()
        new_keys = list(set(exit_keys) - set(enter_keys))
        for new_key in new_keys:
            result[new_key] = os.getenv(new_key)
        return result

    def new_env_vars(self):
        return self._new_env_vars

    def is_creating_env_var(self, name):
        return name in self._new_env_vars.keys()
