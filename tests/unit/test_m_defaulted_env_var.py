from commands import CommandError # avoid cyclic dependency
from env_vars import DefaultedEnvVar

NAME = "HOST"
NOTES = "The hostname of Merkely"


def test_is_not_required():
    _, ev = make_test_variables()
    assert not ev.is_required


def test_value_is_None_when_not_set_in_os():
    _, ev = make_test_variables()
    assert ev.value is None


def test_value_when_set_in_os():
    os_env, ev = make_test_variables()
    not_defaulted = "https://test.merkely.com"
    os_env['MERKELY_'+NAME] = not_defaulted
    assert ev.value == not_defaulted


def make_test_variables():
    os_env = {}
    return os_env, DefaultedEnvVar(os_env, NAME, NOTES)
