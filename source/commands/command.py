from abc import ABC
from collections import namedtuple
from env_vars import *
from errors import ChangeError
import re
import copy


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
    def names(cls):
        return copy.deepcopy(Command.__names)

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
        parts = re.findall('[A-Z][^A-Z]*', cls.__name__)
        Command.__names.append("_".join(part.lower() for part in parts))

    __classes = {}
    __names = []

    # - - - - - - - - - - - - - - - - - - - - -
    # os env-vars

    @property
    def env(self):
        return self._external.env

    # - - - - - - - - - - - - - - - - - - - - -
    # Living documentation

    def summary(self, _ci):  # pragma: no cover
        """
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    @property
    def merkely_env_vars(self):
        """
        All the MERKELY_... env-vars for this command.
        Used in living documentation.
        """
        names = self._merkely_env_var_names
        objects = [getattr(self, name) for name in names]
        return namedtuple('MerkelyEnvVars', tuple(names))(*objects)

    def ci_env_var_names(self, ci):
        """
        All the env-var names used in defaults for all
        the merkely_env_vars for this command, in the given ci.
        Used in living documentation.
        For example, one of LogTest command's merkely_env_vars is
        MERKELY_CI_BUILD_URL which has a default, in ci='github',
        which uses GITHUB_REPOSITORY. So GITHUB_REPOSITORY is one
        of the ci_env_var_names() for LogCommand when ci=='github'
        """
        if ci == 'docker':
            return []
        names = []
        for var in self.merkely_env_vars:
            if isinstance(var, CompoundCiEnvVar):
                names.extend(var.ci_env_var_names(ci))
        return sorted(set(names))

    @property
    def _merkely_env_var_names(self):  # pragma: no cover
        """
        The names of the MERKELY_... env-var names for
        this command, in display-order.
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    def volume_mounts(self, _ci):  # pragma: no cover
        """
        Used in living documentation.
        """
        raise NotImplementedError(self.name)

    # - - - - - - - - - - - - - - - - - - - - -
    # Common merkely env-vars

    @property
    def merkelypipe(self):
        if self.name.string == "declare_pipeline":
            json = self._external.merkelypipe
        else:
            json = {}

        owner = self._required_env_var("MERKELY_OWNER", "...")
        pipeline = self._required_env_var("MERKELY_PIPELINE", "...")
        if owner.string != "" and pipeline.string != "":
            json["owner"] = owner.value
            json["name"] = pipeline.value

        return json

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
    def pipe_path(self):
        # See external.merkelypipe
        name = "MERKELY_PIPE_PATH"
        default = "/data/Merkelypipe.json"
        notes = " ".join([
            f"The full path to your Merkelypipe file.",
            "Must be volume-mounted in the container.",
            f"Defaults to {default}"
        ])
        return self._static_defaulted_env_var(name, default, notes)

    @property
    def user_data(self):
        return UserDataEnvVar(self._external)

    @property
    def is_compliant(self):
        notes = "TRUE if the artifact is considered compliant from you build process."
        return self._required_env_var('MERKELY_IS_COMPLIANT', notes)

    # - - - - - - - - - - - - - - - - - - - - -
    # subclass helpers

    def _required_env_var(self, name, notes):
        return RequiredEnvVar(self.env, name, notes)

    def _static_defaulted_env_var(self, name, default, notes):
        return StaticDefaultedEnvVar(self.env, name, default, notes)

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")

    # - - - - - - - - - - - - - - - - - - - - -
    # Subclass command implementation

    def __call__(self):  # pragma: no cover
        raise NotImplementedError(self.name)

