from collections import namedtuple

from env_vars import DefaultedEnvVar, OptionalEnvVar, RequiredEnvVar, FingerprintEnvVar
from commands import load_json


class Command:
    """
    Abstract Base Class for all merkely/change commands.
    """
    def __init__(self, context):
        self._context = context

    def __call__(self):  # pragma: no cover
        raise NotImplementedError(f"{self._class_name}.__call__(self) subclass override missing")

    def check(self):
        for env_var in self.env_vars:
            env_var.value

    @property
    def env_vars(self):
        names = self._env_var_names
        objects = [getattr(self, name) for name in names]
        return namedtuple('EnvVars', tuple(names))(*objects)

    @property
    def _env_var_names(self):  # pragma: no cover
        raise NotImplementedError(f"{self._class_name}._env_var_names(self) subclass override missing.")

    # - - - - - - - - - - - - - - - - - - - - -
    # common env-vars

    @property
    def name(self):
        description = "The Merkely command to execute."
        return self._required_env_var("COMMAND", description)

    @property
    def api_token(self):
        description = "Your API token for Merkely."
        return self._required_env_var("API_TOKEN", description)

    @property
    def fingerprint(self):
        return FingerprintEnvVar(self)

    @property
    def host(self):
        default = "https://app.compliancedb.com"
        description = f"The host name for Merkely. The default is {default}"
        return self._defaulted_env_var("HOST", default, description)

    @property
    def is_compliant(self):
        description = "Whether this artifact is considered compliant from you build process."
        return self._required_env_var('IS_COMPLIANT', description)

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def merkelypipe(self):
        return load_json("/Merkelypipe.json")

    # - - - - - - - - - - - - - - - - - - - - -
    # context objects

    @property
    def docker_fingerprinter(self):
        return self._context.docker_fingerprinter

    @property
    def file_fingerprinter(self):
        return self._context.file_fingerprinter

    @property
    def env(self):
        return self._context.env

    # - - - - - - - - - - - - - - - - - - - - -

    def _defaulted_env_var(self, name, default, description):
        return DefaultedEnvVar(self.env, f"MERKELY_{name}", default, description)

    def _optional_env_var(self, name, description):
        return OptionalEnvVar(self.env, f"MERKELY_{name}", description)

    def _required_env_var(self, name, description):
        return RequiredEnvVar(self.env, f"MERKELY_{name}", description)

    # - - - - - - - - - - - - - - - - - - - - -

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def _class_name(self):  # pragma: no cover
        return self.__class__.__name__
