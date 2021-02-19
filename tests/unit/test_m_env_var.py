from commands import CommandError
from env_vars import EnvVar
from pytest import raises

NAME = "LEWIS"
NOTES = "A favourite Author"
OS_ENV = {}


def test_name_as_set_in_ctor():
    ev = Example(OS_ENV, NAME, NOTES)
    assert ev.name == 'MERKELY_'+NAME


def test_notes_as_set_in_ctor():
    ev = Example(OS_ENV, NAME, NOTES)
    assert ev.notes() == NOTES


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


class Example(EnvVar):
    def value(self):
        pass

    def is_required(self):
        return True