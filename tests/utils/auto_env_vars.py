import copy
import os


class UnexpectedEnvVarsError(Exception):
    def __init__(self, expected, actual):
        self._expected = expected
        self._actual = actual


class AutoEnvVars(object):
    def __init__(self, enter_vars, expected_new_vars=None):
        """
        Args:
            enter_vars: A dictionary of env-vars to set on entry.
            expected_new_vars: A dictionary of env-vars we expect to be newly set before exit.
        """
        self._original_env_vars = copy.deepcopy(os.environ)
        self._enter_vars = enter_vars
        if expected_new_vars is None:
            self._expected_new_vars = {}
        else:
            self._expected_new_vars = expected_new_vars

    def __enter__(self):
        for (name, value) in self._enter_vars.items():
            os.environ[name] = value
        return self

    def __exit__(self, _type, _value, _traceback):
        actual = self._actual_new_vars()
        self._restore_original_env_vars()
        expected = self._expected_new_vars
        if expected != actual:
            raise UnexpectedEnvVarsError(expected, actual)

    def _restore_original_env_vars(self):
        os.environ.clear()
        for (name, value) in self._original_env_vars.items():
            os.environ[name] = value

    def _actual_new_vars(self):
        result = {}
        for key in os.environ.keys():
            if not key in self._original_env_vars.keys() and not key in self._enter_vars.keys():
                result[key] = os.getenv(key)
        return result
