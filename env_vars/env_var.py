
class EnvVar:
    """
    An abstract base class for 'smart' OS env-vars.
    """
    def __init__(self, env, name, notes, example=None):
        assert name is not None
        assert name != ""
        assert notes is not None
        assert notes != ""
        self._env = env
        self._name = name
        self._notes = notes
        if example is None:
            example = "${...}"
        self._example = example

    @property
    def env(self):
        """
        The underlying OS environment.
        """
        return self._env

    @property
    def name(self):
        """
        Non-empty string, as set in the ctor.
        Used in living documentation.
        Never raises.
        """
        return f"MERKELY_{self._name}"

    @property
    def notes(self):
        """
        Non-empty string as set in the ctor.
        Used in living documentation.
        Never raises.
        """
        return self._notes

    @property
    def example(self):
        return self._example

    @property
    def is_required(self):  # pragma: no cover
        """
        True or False.
        Used in living documentation.
        Never raises.
        """
        raise NotImplementedError(self.name)

    @property
    def value(self):  # pragma: no cover
        """
        run() validates its command by getting the value property
        of each command's env-var. Each env-var's value raises
        if it is invalid.
        """
        raise NotImplementedError(self.name)
