import copy
import os


class ScopedEnvVars(object):
    def __init__(self, new_vars_on_enter, expected_new_vars_on_exit=None):
        """
        Args:
            new_vars_on_enter: A dictionary of new env-vars to set on entry and auto-unset on exit.
            expected_new_vars_on_exit: A dictionary of (different) env-vars we expect to be newly set before exit.
        Raises:
            AlreadyExistingEnvVarError: if, on enter, any new_vars_on_enter key is an already existing env-var.
            UnexpectedEnvVarError: if, on exit, the newly set env-vars do not match expected_new_vars_on_exit.
        """
        if expected_new_vars_on_exit is None:
            expected_new_vars_on_exit = {}
        self._new_vars_on_enter = new_vars_on_enter
        self._expected_new_vars_on_exit = expected_new_vars_on_exit

    def __enter__(self):
        self._original_env_vars = copy.deepcopy(os.environ)
        os.environ.update(self._checked_new_vars_on_enter())
        return os.environ

    def _checked_new_vars_on_enter(self):
        already_exist = {name: value
                         for name, value in os.environ.items()
                         if name in self._new_vars_on_enter.keys()}
        if already_exist != {}:
            raise AlreadyExistingEnvVarError(already_exist)
        else:
            return self._new_vars_on_enter

    def __exit__(self, _type, _value, _traceback):
        actual = self._actual_new_vars()
        self._restore_original_env_vars()
        expected = self._expected_new_vars_on_exit
        if expected != actual:
            raise UnexpectedEnvVarError(expected, actual)

    def _restore_original_env_vars(self):
        os.environ.clear()
        os.environ.update(self._original_env_vars)

    def _actual_new_vars(self):
        return {name: value
                for name, value in os.environ.items()
                if self._is_new(name) or self._has_changed(name, value)}

    def _is_new(self, name):
        return not name in self._original_env_vars.keys() and not name in self._new_vars_on_enter.keys()

    def _has_changed(self, name, value):
        return name in self._new_vars_on_enter.keys() and self._new_vars_on_enter[name] != value


class AlreadyExistingEnvVarError(RuntimeError):
    def __init__(self, env_vars):
        self._env_vars = env_vars

    def env_vars(self):
        return self._env_vars


class UnexpectedEnvVarError(RuntimeError):
    def __init__(self, expected, actual):
        self._expected = expected
        self._actual = actual

    def expected(self):
        return self._expected

    def actual(self):
        return self._actual
