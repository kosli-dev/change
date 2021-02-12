import abc


class EnvVar(abc.ABC):
    """
    An abstract base class for 'smart' OS env-vars.
    """
    def __init__(self, env, name, notes, example=None):
        assert name is not None
        assert name != ""
        assert notes is not None
        assert notes != ""
        self.__env = env
        self.__name = name
        self.__notes = notes
        if example is None:
            example = "${...}"
        self.__example = example

    def __get(self, default):
        return self.__env.get(self.name, default)

    @property
    def is_set(self):
        return self.__get(None) is not None

    @property
    def string(self):
        return self.__get("")

    @property
    def is_empty(self):
        return self.string == ""

    @property
    def name(self):
        """
        Non-empty string, as set in the ctor.
        Used in living documentation.
        Never raises.
        """
        return f"MERKELY_{self.__name}"

    @property
    def notes(self):
        """
        Non-empty string as set in the ctor.
        Used in living documentation.
        Never raises.
        """
        return self.__notes

    @property
    def example(self):
        return self.__example

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
