from env_vars import DefaultedEnvVar

NAME = "MERKELY_HOST"
DEFAULT = "https://default.merkely.com"
DESCRIPTION = "The hostname of Merkely"


def test_type_is_defaulted():
    _, ev = make_test_variables()
    assert ev.type == 'defaulted'


def test_name_as_set_in_ctor():
    _, ev = make_test_variables()
    assert ev.name == NAME


def test_description_as_set_in_ctor():
    _, ev = make_test_variables()
    assert ev.description == DESCRIPTION


def test_value_from_default_when_not_set_in_os():
    _, ev = make_test_variables()
    assert ev.value == DEFAULT


def test_value_when_set_in_os():
    os_env, ev = make_test_variables()
    not_default = "https://test.merkely.com"
    os_env[NAME] = not_default
    assert ev.value == not_default


def make_test_variables():
    os_env = {}
    return os_env, DefaultedEnvVar(os_env, NAME, DEFAULT, DESCRIPTION)
