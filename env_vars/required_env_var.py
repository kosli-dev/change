from commands import CommandError
from env_vars import EnvVar


class RequiredEnvVar(EnvVar):
    """
    Represents a required OS environment-variable that
    contributes something to its parent Command's http payload.
    """
    def __init__(self, env, name, description):
        super().__init__(env, name, description)

    @property
    def type(self):
        return 'required'

    @property
    def value(self):
        """
        The OS env-var for name if present and a non empty string.
        Raises if not present or the empty string.
        """
        result = self.env.get(self.name, None)
        if result is None:
            raise CommandError(f"{self.name} environment-variable is not set.")
        elif result == "":
            raise CommandError(f"{self.name} environment-variable is empty string.")
        else:
            return result
