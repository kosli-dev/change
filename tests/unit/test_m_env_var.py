from commands import CommandError
from env_vars import EnvVar
from pytest import raises

NAME = "MERKELY_LEWIS"
NOTES = "A favourite Author"
OS_ENV = {}

def test_name_as_set_in_ctor():
    ev = EnvVar(OS_ENV, NAME, NOTES)
    assert ev.name == NAME


def test_notes_as_set_in_ctor():
    ev = EnvVar(OS_ENV, NAME, NOTES)
    assert ev.notes == NOTES


def test_no_name_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, None, NOTES)


def test_empty_name_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, "", NOTES)


def test_no_notes_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, NAME, None)


def test_empty_notes_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, NAME, "")
