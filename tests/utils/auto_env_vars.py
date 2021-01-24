import copy
import os


CDB_DRY_RUN = {"CDB_DRY_RUN": "TRUE"}


class AutoEnvVars(object):
    def __init__(self, new_vars_on_enter, expected_new_vars_on_exit={}):
        """
        Args:
            new_vars_on_enter: A dictionary of new env-vars to set on entry and auto-unset on exit.
            expected_new_vars_on_exit: A dictionary of (different) env-vars we expect to be newly set before exit.
        Raises:
            AlreadyExistingEnvVar: if, on enter, any new_vars_on_enter key is an already existing env-var.
            UnexpectedEnvVar: if, on exit, the newly set env-vars do not match expected_new_vars_on_exit.
        """
        self._new_vars_on_enter = new_vars_on_enter
        self._expected_new_vars_on_exit = expected_new_vars_on_exit

    def __enter__(self):
        self._original_env_vars = copy.deepcopy(os.environ)
        for (name, value) in self._checked_new_vars_on_enter().items():
            os.environ[name] = value
        return self

    def _checked_new_vars_on_enter(self):
        already_exist = {}
        for name in self._new_vars_on_enter:
            if name in os.environ.keys():
                already_exist[name] = os.environ[name]
        if already_exist != {}:
            raise AlreadyExistingEnvVar(already_exist)
        else:
            return self._new_vars_on_enter

    def __exit__(self, _type, _value, _traceback):
        actual = self._actual_new_vars()
        self._restore_original_env_vars()
        expected = self._expected_new_vars_on_exit
        if expected != actual:
            raise UnexpectedEnvVar(expected, actual)

    def _restore_original_env_vars(self):
        os.environ.clear()
        for (name, value) in self._original_env_vars.items():
            os.environ[name] = value

    def _actual_new_vars(self):
        result = {}
        for (name, value) in os.environ.items():
            if self._is_new(name) or self._has_changed(name, value):
                result[name] = value
        return result

    def _is_new(self, name):
        return not name in self._original_env_vars.keys() and not name in self._new_vars_on_enter.keys()

    def _has_changed(self, name, value):
        return name in self._new_vars_on_enter.keys() and self._new_vars_on_enter[name] != value


class AlreadyExistingEnvVar(Exception):
    def __init__(self, vars):
        self._vars = vars

    def vars(self):
        return self._vars


class UnexpectedEnvVar(Exception):
    def __init__(self, expected, actual):
        self._expected = expected
        self._actual = actual

    def expected(self):
        return self._expected

    def actual(self):
        return self._actual
