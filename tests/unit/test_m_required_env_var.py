from errors import ChangeError
from env_vars import RequiredEnvVar
from pytest import raises

NAME = "MERKELY_MORSE"
NOTES = "A favourite tv program"


def test_is_required():
    _, ev = make_test_variables()
    assert ev.is_required


def test_value_when_set_to_non_empty_in_os():
    os_env, ev = make_test_variables()
    expected = 'value-set-from-os'
    os_env[NAME] = expected
    assert ev.value == expected


def test_value_raises_when_set_to_empty_in_os():
    os_env, ev = make_test_variables()
    os_env[NAME] = ""
    with raises(ChangeError) as exc:
        ev.value
    assert str(exc.value) == f"{NAME} environment-variable is empty string."


def test_value_raises_when_not_set_in_os():
    _, ev = make_test_variables()
    with raises(ChangeError) as exc:
        ev.value
    assert str(exc.value) == f"{NAME} environment-variable is not set."


def make_test_variables():
    os_env = {}
    return os_env, RequiredEnvVar(os_env, NAME, NOTES)
