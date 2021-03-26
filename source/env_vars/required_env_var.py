from errors import ChangeError
from env_vars import EnvVar


class RequiredEnvVar(EnvVar):
    """
    A required OS environment-variable.
    """
    def __init__(self, env, name):
        super().__init__(env, name)

    def is_required(self, _ci_name):
        return True

    @property
    def value(self):
        """
        The OS env-var for name if present and non empty.
        Raises if not present or empty.
        """
        if self.is_unset:
            raise ChangeError(f"{self.name} environment-variable is not set.")
        elif self.is_empty:
            raise ChangeError(f"{self.name} environment-variable is empty string.")
        else:
            return self.string

    @property
    def is_unset(self):
        """
        Returns true if this environment-variable is unset.
        Note: returns false if the environment-variable
        is set, but to the empty string.
        """
        return self._get(default=None) is None
