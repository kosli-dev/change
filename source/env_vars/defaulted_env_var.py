from env_vars import EnvVar


class DefaultedEnvVar(EnvVar):
    """
    A defaulted OS environment-variable.
    """
    def __init__(self, env, name):
        super().__init__(env, name)

    def is_required(self, _ci_name):
        return False
