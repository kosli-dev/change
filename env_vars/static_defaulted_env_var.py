from env_vars import DefaultedEnvVar


class StaticDefaultedEnvVar(DefaultedEnvVar):
    """
    A defaulted OS environment-variable where
    the default is statically assigned at construction.
    """
    def __init__(self, env, name, default, notes):
        super().__init__(env, name, notes)
        self._default = default

    @property
    def value(self):
        if self._is_set:
            return super().value
        else:
            return self._default
