from env_vars import EnvVar
from pytest import raises

NAME = "MERKELY_LEWIS"
OS_ENV = {}


def test_name_as_set_in_ctor():
    ev = Example(OS_ENV, NAME)
    assert ev.name == NAME


def test_no_name_is_programmer_error():
    with raises(AssertionError):
        ev = Example(OS_ENV, None)


def test_empty_name_is_programmer_error():
    with raises(AssertionError):
        ev = Example(OS_ENV, "")


def test_string_is_empty_when_not_set():
    env = {}
    assert Example(env, NAME).string == ""


def test_string_is_empty_when_set_to_empty_string():
    env = {NAME: ""}
    assert Example(env, NAME).string == ""


class Example(EnvVar):
    def value(self):
        pass  # pragma: no cover

    def is_required(self):
        return True  # pragma: no cover

    def doc_example(self, _ci_name, _command_name):
        return True, ""  # pragma: no cover

    def doc_note(self, _ci_name, _command_name):
        return ""  # pragma: no cover
