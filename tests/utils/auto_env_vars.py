import copy
import os


class AlreadyExistingEnvVarOnEnterError(Exception):
    def __init__(self, vars):
        self._vars = vars

    def vars(self):
        return self._vars


class UnexpectedEnvVarSetOnExitError(Exception):
    def __init__(self, expected, actual):
        self._expected = expected
        self._actual = actual

    def expected(self):
        return self._expected

    def actual(self):
        return self._actual


CDB_DRY_RUN = {"CDB_DRY_RUN": "TRUE"}


class AutoEnvVars(object):
    def __init__(self, new_enter_vars, expected_exit_new_vars=None):
        """
        Args:
            enter_vars: A dictionary of env-vars to set on entry.
            expected_new_vars: A dictionary of env-vars we expect to be newly set before exit.
        """
        self._original_env_vars = copy.deepcopy(os.environ)
        self._new_enter_vars = new_enter_vars
        if expected_exit_new_vars is None:
            self._expected_exit_new_vars = {}
        else:
            self._expected_exit_new_vars = expected_exit_new_vars

    def __enter__(self):
        for (name, value) in self._checked_new_env_vars().items():
            os.environ[name] = value
        return self

    def __exit__(self, _type, _value, _traceback):
        actual = self._actual_new_vars()
        self._restore_original_env_vars()
        expected = self._expected_exit_new_vars
        if expected != actual:
            raise UnexpectedEnvVarSetOnExitError(expected, actual)

    def _checked_new_env_vars(self):
        already_exist = {}
        for name in self._new_enter_vars:
            if name in os.environ.keys():
                already_exist[name] = os.environ[name]
        if already_exist != {}:
            raise AlreadyExistingEnvVarOnEnterError(already_exist)
        else:
            return self._new_enter_vars

    def _restore_original_env_vars(self):
        os.environ.clear()
        for (name, value) in self._original_env_vars.items():
            os.environ[name] = value

    def _actual_new_vars(self):
        result = {}
        for key in os.environ.keys():
            if not key in self._original_env_vars.keys() and not key in self._new_enter_vars.keys():
                result[key] = os.getenv(key)
        return result
