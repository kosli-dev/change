from commands import EnvVar, CommandError


class RequiredEnvVar(EnvVar):
    def __init__(self, command, name, description):
        super().__init__(command, name, description)

    @property
    def value(self):
        result = self._env.get(self.name, None)
        if result is None:
            raise CommandError(f"{self.name} environment-variable is not set.")
        if result == "":
            raise CommandError(f"{self.name} environment-variable is empty string.")
        return result
