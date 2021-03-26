from env_vars import DefaultedEnvVar


class StaticDefaultedEnvVar(DefaultedEnvVar):
    """
    A defaulted OS environment-variable where
    the default is statically assigned at construction.
    """
    def __init__(self, env, name, default):
        super().__init__(env, name)
        self.__default = default

    @property
    def value(self):
        if self.string != "":
            return self.string
        else:
            return self.__default
