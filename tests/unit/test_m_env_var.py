from env_vars import EnvVar
from pytest import raises

NAME = "MERKELY_LEWIS"
NOTES = "A favourite Author"
OS_ENV = {}


def test_name_as_set_in_ctor():
    ev = Example(OS_ENV, NAME, NOTES)
    assert ev.name == NAME


def test_notes_as_set_in_ctor():
    ev = Example(OS_ENV, NAME, NOTES)
    assert ev.notes('github') == NOTES


def test_no_name_is_programmer_error():
    with raises(AssertionError):
        ev = Example(OS_ENV, None, NOTES)


def test_empty_name_is_programmer_error():
    with raises(AssertionError):
        ev = Example(OS_ENV, "", NOTES)


def test_no_notes_allows_subclass_override():
    Example(OS_ENV, NAME, None)


def test_empty_notes_allows_subclass_override():
    Example(OS_ENV, NAME, "")


def test_string_is_empty_when_not_set():
    env = {}
    assert Example(env, NAME, NOTES).string == ""


def test_string_is_empty_when_set_to_empty_string():
    env = {NAME: ""}
    assert Example(env, NAME, NOTES).string == ""


class Example(EnvVar):
    def value(self):
        pass

    def is_required(self):
        return True

    def doc_example(self, _ci_name, _command_name):
        return True, ""

    def doc_note(self, _ci_name, _command_name):
        return ""
