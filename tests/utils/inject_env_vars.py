import copy
import os


class AlreadyExistingEnvVars(Exception):
    def __init__(self, vars):
        self._vars = vars

    def already_existing(self):
        return self._vars


def inject_env_vars(env_vars):
    def raise_if_any_already_exist():
        already_exist = {key: os.environ[key] for key in env_vars.keys() & os.environ.keys()}
        if already_exist != {}:
            raise AlreadyExistingEnvVars(already_exist)

    def add_to_environ(all):
        for (name, value) in all.items():
            os.environ[name] = value

    def decorator(f):
        def wrapper(*args, **kwargs):
            raise_if_any_already_exist()
            original_env_vars = copy.deepcopy(os.environ)
            add_to_environ(env_vars)
            try:
                result = f(*args, **kwargs)
            finally:
                os.environ.clear()
                add_to_environ(original_env_vars)
            return result
        return wrapper
    return decorator
