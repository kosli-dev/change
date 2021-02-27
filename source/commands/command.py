from abc import ABC
from collections import namedtuple
from env_vars import *
from errors import ChangeError


class Command(ABC):
    """
    Abstract Base Class for all merkely/change commands.
    """
    def __init__(self, external):
        self._external = external

    # - - - - - - - - - - - - - - - - - - - - -
    # Class methods

    @classmethod
    def all(cls):
        return Command.__classes

    @classmethod
    def named(_cls, string):
        name = "".join(list(s.capitalize() for s in string.split('_')))
        try:
            return Command.__classes[name]
        except KeyError:
            raise ChangeError(f"Unknown command: {string}")

    def __init_subclass__(cls):
        super().__init_subclass__()
        Command.__classes[cls.__name__] = cls

    __classes = {}

    # - - - - - - - - - - - - - - - - - - - - -
    # Merkelypipe.json

    @property
    def merkelypipe(self):
        return self._external.merkelypipe

    # - - - - - - - - - - - - - - - - - - - - -
    # All merkely env-vars

    @property
    def merkely_env_vars(self):
        names = self._merkely_env_var_names
        objects = [getattr(self, name) for name in names]
        return namedtuple('MerkelyEnvVars', tuple(names))(*objects)

    # - - - - - - - - - - - - - - - - - - - - -
    # Common merkely env-vars

    @property
    def api_token(self):
        notes = "Your API token for Merkely."
        return self._required_env_var("MERKELY_API_TOKEN", notes)

    @property
    def ci_build_url(self):
        return CIBuildUrlEnvVar(self.env)

    @property
    def fingerprint(self):
        return FingerprintEnvVar(self._external)

    @property
    def host(self):
        return HostEnvVar(self.env)

    @property
    def name(self):
        notes = "The Merkely command to execute."
        return self._required_env_var("MERKELY_COMMAND", notes)

    @property
    def user_data(self):
        return UserDataEnvVar(self._external)

    @property
    def is_compliant(self):
        notes = "TRUE if the artifact is considered compliant from you build process."
        return self._required_env_var('MERKELY_IS_COMPLIANT', notes)

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def env(self):
        return self._external.env

    def _required_env_var(self, name, notes):
        return RequiredEnvVar(self.env, name, notes)

    def _static_defaulted_env_var(self, name, default, notes):
        return StaticDefaultedEnvVar(self.env, name, default, notes)

    # - - - - - - - - - - - - - - - - - - - - -
    # Living documentation

    @property
    def summary(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    def invocation(self, type):
        tab = "    "
        def lcnl(string):
            line_continuation = "\\"
            newline = "\n"
            return f"{string} {line_continuation}{newline}"
        def env(var):
            if var.name == "MERKELY_COMMAND":
                value = var.value
            else:
                value = '"' + "${" + var.name + "}" + '"'
            return lcnl(f'{tab}--env {var.name}={value}')

        invocation_string = lcnl("docker run")
        for name in self._merkely_env_var_names:
            var = getattr(self, name)
            if type == 'full':
                invocation_string += env(var)
            if type == 'minimum' and var.is_required:
                invocation_string += env(var)

        invocation_string += lcnl(f"{tab}--rm")
        for mount in self._volume_mounts:
            invocation_string += lcnl(f"{tab}--volume {mount}")
        invocation_string += lcnl(tab+"--volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json")
        invocation_string += f"{tab}merkely/change"
        return invocation_string

    @property
    def _volume_mounts(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    # - - - - - - - - - - - - - - - - - - - - -
    # Subclass implementations

    def __call__(self):  # pragma: no cover
        raise NotImplementedError(self.name)

    @property
    def _merkely_env_var_names(self):  # pragma: no cover
        raise NotImplementedError(self.name)

