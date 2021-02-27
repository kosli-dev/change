from errors import ChangeError
from env_vars import EnvVar, CiEnvVar
from abc import ABC, abstractmethod


class DynamicCiEnvVar(EnvVar, ABC):

    def __init__(self, env, name, notes):
        super().__init__(env, name, '')
        self._notes = notes

    # - - - - - - - - - - - - - - - - - - - - -
    # Living documentation

    def notes(self, ci):
        if ci == 'docker':
            return self._notes
        if ci not in self._ci_env_vars.keys():
            raise RuntimeError(f"{ci} is unknown CI")
        return f"{self._notes} Defaults to {self._ci_env_vars[ci].string}."

    def is_required(self, ci):
        return ci == 'docker'

    def ci_env_var_names(self, ci):
        return self._ci_env_vars[ci].names

    # - - - - - - - - - - - - - - - - - - - - -

    @property
    def value(self):
        if self.string != "":
            return self.string
        else:
            return self.ci_env_var.value

    @property
    def ci_env_var(self):
        return self._ci_env_vars[self.ci]

    @property
    def ci(self):
        if self.on_bitbucket and self.on_github:
            raise self._cannot_expand_error("there are BITBUCKET_ and GITHUB_ env-vars")
        if not self.on_bitbucket and not self.on_github:
            raise self._cannot_expand_error("there are no BITBUCKET_ or GITHUB_ env-vars")
        if self.on_github:
            return 'github'
        if self.on_bitbucket:
            return 'bitbucket'

    @property
    def on_github(self):
        return self._on_ci('GITHUB_')

    @property
    def on_bitbucket(self):
        return self._on_ci('BITBUCKET_')

    def _on_ci(self, name):
        return len(list(key for key in self._env.keys() if key.startswith(name))) > 0

    def _cannot_expand_error(self, ending):
        return ChangeError(
            f"{self.name} env-var is not set "
            "and cannot be default-expanded as the CI system "
            f"cannot be determined ({ending})."
        )

    @abstractmethod
    def _ci_env_vars(self):
        """
        """