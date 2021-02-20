from abc import ABC, abstractmethod
from env_vars import EnvVar
import os

NAME = "MERKELY_ARTIFACT_GIT_COMMIT"
NOTE = "The sha of the git commit that produced this build."


class DynamicEnvVar(EnvVar, ABC):

    def __init__(self, env, name, notes):
        super().__init__(env, name, '')
        self._notes = notes

    def notes(self, ci):
        if ci is 'docker':
            return NOTE
        else:
            return f"{NOTE}. Defaults to {self._ci_env_vars[ci].string}."

    def is_required(self, ci):
        return ci == 'docker'

    @property
    def value(self):
        if self.string != "":
            return self.string
        else:
            return self._ci_env_var.value

    @property
    def _ci_env_var(self):
        return self._ci_env_vars[self._ci]

    @property
    def _ci(self):
        on_github = len(list(key for key in os.environ.keys() if key.startswith('GITHUB_'))) > 0
        if on_github:
            return 'github'
        on_bitbucket = len(list(key for key in os.environ.keys() if key.startswith('BITBUCKET_'))) > 0
        if on_bitbucket:
            return 'bitbucket'

    @abstractmethod
    def _ci_env_vars(self):
        """
        """