import copy
import os


class UnexpectedEnvVarsError(Exception):
    def __init__(self, expected, actual):
        self._expected = expected
        self._actual = actual


class AutoEnvVars(object):
    def __init__(self, env_vars):
        self._true_env_vars = copy.deepcopy(os.environ)
        self._auto_env_vars = env_vars

    def __enter__(self):
        for (name, value) in self._auto_env_vars.items():
            os.environ[name] = value
        return self

    def __exit__(self, _type, _value, _traceback):
        actual = self._actual_set_env_vars()
        os.environ.clear()
        for (name, value) in self._true_env_vars.items():
            os.environ[name] = value
        #expected = self._expected_set_env_vars
        #if expected != actual:
        #    raise UnexpectedEnvVarsError(expected, actual)

    def _actual_set_env_vars(self):
        result = {}
        enter_keys = self._true_env_vars.keys()
        exit_keys = os.environ.keys()
        new_keys = list(set(exit_keys) - set(enter_keys))
        for new_key in new_keys:
            result[new_key] = os.getenv(new_key)
        return result
