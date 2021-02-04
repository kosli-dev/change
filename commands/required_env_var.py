from commands import EnvVar, CommandError


class RequiredEnvVar(EnvVar):
    def __init__(self, name, env, description=None):
        super().__init__(name, env, description)

    @property
    def value(self):
        result = self._env.get(self.name, None)
        if result is None:
            raise CommandError(f"{self.name} environment-variable not set")
        if result == "":
            raise CommandError(f"{self.name} environment-variable is empty string")
        return result
