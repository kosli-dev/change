from commands import EnvVar, CommandError


class RequiredEnvVar(EnvVar):
    def __init__(self, env, name, description):
        super().__init__(env, name, description)

    @property
    def value(self):
        result = self.env.get(self.name, None)
        if result is None:
            raise CommandError(f"{self.name} environment-variable is not set.")
        elif result == "":
            raise CommandError(f"{self.name} environment-variable is empty string.")
        else:
            return result
