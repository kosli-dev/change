from env_vars import OptionalEnvVar

NAME = "MERKELY_LEWIS"
DESCRIPTION = "A favourite Author"


def test_type_is_optional():
    _, ev = make_test_variables()
    assert ev.type == 'optional'


def test_value_when_set_in_os():
    os_env, ev = make_test_variables()
    expected = 'value-set-from-os'
    os_env[NAME] = expected
    assert ev.value == expected
    assert ev.is_present


def test_value_is_None_when_not_set_in_os():
    _, ev = make_test_variables()
    assert ev.value is None
    assert not ev.is_present


def make_test_variables():
    os_env = {}
    return os_env, OptionalEnvVar(os_env, NAME, DESCRIPTION)
