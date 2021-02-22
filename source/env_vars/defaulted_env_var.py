from env_vars import EnvVar


class DefaultedEnvVar(EnvVar):
    """
    A defaulted OS environment-variable.
    """
    def __init__(self, env, name, notes):
        super().__init__(env, name, notes)

    def is_required(self, ci):
        return False
