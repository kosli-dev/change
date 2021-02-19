from errors import ChangeError
from env_vars import EnvVar


class RequiredEnvVar(EnvVar):
    """
    A required OS environment-variable.
    """
    def __init__(self, env, name, notes, example=None):
        super().__init__(env, name, notes, example)

    @property
    def is_required(self):
        return True

    @property
    def value(self):
        """
        The OS env-var for name if present and non empty.
        Raises if not present or empty.
        """
        if not self.is_set:
            raise ChangeError(f"{self.name} environment-variable is not set.")
        elif self.is_empty:
            raise ChangeError(f"{self.name} environment-variable is empty string.")
        else:
            return self.string
