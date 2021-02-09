from commands import CommandError
from env_vars import EnvVar


class RequiredEnvVar(EnvVar):
    """
    Represents a required OS environment-variable.
    Retrieving its value property will raise if it does not exist.
    Contributes something to its parent Command's http payload.
    """
    def __init__(self, env, name, description):
        super().__init__(env, name, description)

    @property
    def type(self):
        return 'required'

    @property
    def value(self):
        result = self.env.get(self.name, None)
        if result is None:
            raise CommandError(f"{self.name} environment-variable is not set.")
        elif result == "":
            raise CommandError(f"{self.name} environment-variable is empty string.")
        else:
            return result
