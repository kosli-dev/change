from commands import CommandError
from env_vars import EnvVar
from pytest import raises

NAME = "MERKELY_LEWIS"
DESCRIPTION = "A favourite Author"
OS_ENV = {}

def test_name_as_set_in_ctor():
    ev = EnvVar(OS_ENV, NAME, DESCRIPTION)
    assert ev.name == NAME


def test_description_as_set_in_ctor():
    ev = EnvVar(OS_ENV, NAME, DESCRIPTION)
    assert ev.description == DESCRIPTION


def test_no_name_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, None, DESCRIPTION)


def test_empty_name_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, "", DESCRIPTION)


def test_no_description_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, NAME, None)


def test_empty_description_is_programmer_error():
    with raises(AssertionError):
        ev = EnvVar(OS_ENV, NAME, "")
