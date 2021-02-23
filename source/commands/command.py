from abc import ABC
from collections import namedtuple
from env_vars import *
from commands import load_json


class Command(ABC):
    """
    Abstract Base Class for all merkely/change commands.
    """
    def __init__(self, context):
        self.__context = context

    def __call__(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    @property
    def env(self):
        return self.__context.env

    @property
    def env_vars(self):
        names = self._env_var_names
        objects = [getattr(self, name) for name in names]
        return namedtuple('EnvVars', tuple(names))(*objects)

    @property
    def _env_var_names(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    # - - - - - - - - - - - - - - - - - - - - -
    # common env-vars

    @property
    def name(self):
        notes = "The Merkely command to execute."
        return self._required_env_var("MERKELY_COMMAND", notes)

    @property
    def api_token(self):
        notes = "Your API token for Merkely."
        return self._required_env_var("MERKELY_API_TOKEN", notes)

    @property
    def fingerprint(self):
        return FingerprintEnvVar(self.__context)

    @property
    def host(self):
        return HostEnvVar(self.env)

    @property
    def is_compliant(self):
        notes = "TRUE if the artifact is considered compliant from you build process."
        return self._required_env_var('MERKELY_IS_COMPLIANT', notes)

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def merkelypipe(self):
        import os
        if os.path.exists("/Merkelypipe.json"):
            return load_json("/Merkelypipe.json")
        if os.path.exists("/data/Merkelypipe.json"):
            return load_json("/data/Merkelypipe.json")
        from errors import ChangeError
        raise ChangeError("Merkelypipe.json file not found.")

    # - - - - - - - - - - - - - - - - - - - - -

    def _required_env_var(self, name, notes):
        return RequiredEnvVar(self.env, name, notes)

    def _static_defaulted_env_var(self, name, default, notes):
        return StaticDefaultedEnvVar(self.env, name, default, notes)

    def _defaulted_env_var(self, name, notes):
        return DefaultedEnvVar(self.env, name, notes)

    # - - - - - - - - - - - - - - - - - - - - -

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")
